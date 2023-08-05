import sys
import enviral


def main():
    schemas = []
    for schema in reversed(sys.argv):
        if schema.endswith("json-schema-env-validator"):
            break
        schemas.append(schema)
    enviral.validate_env(*list(reversed(schemas)))
