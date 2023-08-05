import json
import os
import pathlib
import typing

import jsonschema

from .structures import CaseInsensitiveDict


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return jsonschema.validators.extend(validator_class, {"properties": set_defaults})


DefaultValidatingDraft7Validator = extend_with_default(jsonschema.Draft7Validator)


def resolve_dotted_name(name: str):
    """
    import the provided dotted name

    >>> resolve_dotted_name('guillotina.interfaces.IRequest')
    <InterfaceClass guillotina.interfaces.IRequest>

    :param name: dotted name
    """
    if not isinstance(name, str):
        return name  # already an object
    names = name.split(".")
    used = names.pop(0)
    found = __import__(used)
    for n in names:
        used += "." + n
        try:
            found = getattr(found, n)
        except AttributeError:
            __import__(used)
            found = getattr(found, n)

    return found


def resolve_path(file_path: str) -> pathlib.Path:
    """
    Resolve path to file inside python module

    >>> resolve_path('guillotina:__init__.py')
    PosixPath('/Users/vangheem/onna/onna-canonical/libsrc/guillotina/guillotina/__init__.py')

    :param file_path: `module:path` string
    """
    if ":" in file_path:
        # referencing a module
        dotted_mod_name, _, rel_path = file_path.partition(":")
        module = resolve_dotted_name(dotted_mod_name)
        if module is None:
            raise Exception("Invalid module for static directory {}".format(file_path))
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(module.__file__)), rel_path
        )
    return pathlib.Path(file_path)


def _get_schema(schema: typing.Union[str, typing.Dict]) -> typing.Dict:
    """
    Needs to be able to resolve and read schemas from python modules
    """
    if isinstance(schema, str):
        if ":" in schema:
            schema = resolve_path(schema)
        with open(schema) as fi:
            schema = json.loads(fi.read())
    return schema


def serialize(
    *schemas: typing.Union[str, typing.Dict], prefix=""
) -> typing.Dict[str, typing.Any]:
    prefix = prefix.lower()
    # use only top-level properties to load from...
    result = {}
    for schema in schemas:
        schema = _get_schema(schema)

        for key, value in os.environ.items():
            key = key.lower()
            if not key.startswith(prefix):
                continue
            start = len(prefix)
            key = key[start:]
            if key in schema["properties"]:
                schema_type = schema["properties"][key].get("type")
                if schema_type == "number":
                    try:
                        if "." in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        # we attempt but ignore error
                        # allow validation to catch properly
                        pass
                if schema_type in ("object", "array"):
                    value = json.loads(value)
                if schema_type == "boolean":
                    value = value.lower() in ("1", "y", "yes", "true")
                result[key] = value

        # run the validator here because we want defaults filled
        try:
            validator = DefaultValidatingDraft7Validator(schema)
            validator.validate(result)
        except jsonschema.exceptions.ValidationError:
            pass
    return result


def validate_env(*schemas: str, prefix="") -> typing.Dict[str, typing.Any]:
    obj = serialize(*schemas, prefix=prefix)
    validate_object(obj, *schemas)
    return obj


def validate_object(obj, *schemas: str) -> typing.Dict[str, typing.Any]:
    for schema in schemas:
        schema = _get_schema(schema)
        validator = DefaultValidatingDraft7Validator(schema)
        validator.validate(obj)
    return obj


_environ = CaseInsensitiveDict()


def get_env(name, default=None):
    if len(_environ) == 0:
        _environ.update(os.environ)
    return _environ.get(name, default)
