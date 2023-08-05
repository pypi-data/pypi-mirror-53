import sys
import enviral


def main():
    schemas = []
    for schema in reversed(sys.argv):
        if schema.endswith("enviral"):
            break
        schemas.append(schema)
    enviral.validate_env(*list(reversed(schemas)))
