import os

import jsonschema
import pytest

import enviral


def test_validate_from_env(env):
    os.environ["FOO"] = "bar"
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string"}, "bar": {"type": "string"}},
        "required": ["foo", "bar"],
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        enviral.validate_env(schema)

    os.environ["BAR"] = "foo"
    enviral.validate_env(schema)


def test_validate_int_from_env(env):
    os.environ["FOO"] = "bar"
    schema = {"type": "object", "properties": {"foo": {"type": "number"}}}
    with pytest.raises(jsonschema.exceptions.ValidationError):
        enviral.validate_env(schema)

    os.environ["FOO"] = "2"
    settings = enviral.validate_env(schema)
    assert settings["foo"] == 2
