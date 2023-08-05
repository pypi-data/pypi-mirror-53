import enviral
import os


def test_get_setting_from_env(env):
    os.environ["FOO"] = "bar"
    settings = enviral.serialize(
        {"type": "object", "properties": {"foo": {"type": "string"}}}
    )
    assert "FOO" not in settings
    assert "foo" in settings
    assert settings["foo"] == "bar"


def test_get_setting_from_env_with_prefix(env):
    os.environ["PREFIX_FOO"] = "bar"
    settings = enviral.serialize(
        {"type": "object", "properties": {"foo": {"type": "string"}}}, prefix="PREFIX_"
    )
    assert "FOO" not in settings
    assert "foo" in settings
    assert settings["foo"] == "bar"


def test_convert_int_setting_from_env(env):
    os.environ["FOO"] = "2"
    settings = enviral.serialize(
        {"type": "object", "properties": {"foo": {"type": "number"}}}
    )
    assert settings["foo"] == 2


def test_convert_object_setting_from_env(env):
    os.environ["FOO"] = '{"foo": "bar"}'
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {
                "foo": {"type": "object", "properties": {"foo": {"type": "string"}}}
            },
        }
    )
    assert settings["foo"] == {"foo": "bar"}


def test_convert_list_setting_from_env(env):
    os.environ["FOO"] = '["foo", "bar"]'
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {"foo": {"type": "array", "items": {"type": "string"}}},
        }
    )
    assert settings["foo"] == ["foo", "bar"]


def test_convert_bool_setting_from_env(env):
    for setting in ("1", "true", "TRUE", "y", "YES"):
        os.environ["FOO"] = setting
        settings = enviral.serialize(
            {"type": "object", "properties": {"foo": {"type": "boolean"}}}
        )
        assert settings["foo"] is True

    for setting in ("0", "false", "FALSE", "n", "no"):
        os.environ["FOO"] = setting
        settings = enviral.serialize(
            {"type": "object", "properties": {"foo": {"type": "boolean"}}}
        )
        assert settings["foo"] is False


def test_get_json_from_module_file(env):
    os.environ["FOOBAR"] = "bar"
    settings = enviral.serialize("enviral:test-env-schema.json")
    assert settings["foobar"] == "bar"


def test_fill_default_json_schema_value(env):
    os.environ["FOO"] = "bar"
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {
                "foo": {"type": "string"},
                "bar": {"type": "string", "default": "foo"},
            },
        }
    )
    assert settings == {"foo": "bar", "bar": "foo"}
