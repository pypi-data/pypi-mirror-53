# JSON Schema Application Environment Configuration and Validation

This package allows you to validate application environment variables that are
used for configuration with JSON schemas.

It is extremely useful to use with Docker/kubernetes where you might have
quite a bit of configuration originating from environment variables; however,
it also provides a nice generic way to define and validate any application
configuration with JSON Schema.


## Usage

First, define a JSON Schema file(`env-schema.json`):

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#", 
    "type": "object",
  
    "properties": {
        "db_uri": {
            "type": "string",
            "title": "AMQP host"
        }
    },
    "required": ["db_uri"]
}
```

Then, validate your environment config(`export DB_URI=postgresql://localhost:5432`):

```python
import enviral
settings = enviral.validate_env('env-schema.json')
settings['db_uri']
```

Validate with multiple files:

```python
import enviral
settings = enviral.validate_env('env-schema.json', 'package:validation-file.json')
```

You can also validate existing objects against JSON schema files:

```python
import enviral
enviral.validate_object({"db_uri": "postgresql://localhost:5432"}, 'env-schema.json')
```

Or command line validate:

```bash
json-schema-env-validator env-schema.json package:validation-file.json
```

## Development

```bash
pip install -r requirements.txt
pip install -e .
./bin/pre-commit install
```
