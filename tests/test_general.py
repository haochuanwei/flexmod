"""
Simple tests.
"""
import os
import flexmod
from flexmod import ConfigValue, AutolockedConfigValue, Config, ConfigIndex

DIR_PATH = os.path.dirname(__file__)


def config_value_example_num_apples(name="num_apples"):
    return AutolockedConfigValue(name, "number of apples", 0, preprocessor=lambda x: x, validation=lambda x: isinstance(x, int))


class TestAutoInterpret:
    def test_json(self):
        assert flexmod.auto_interpret('{"a": 1}') == {"a": 1}

    def test_list(self):
        assert flexmod.auto_interpret("[1, 2, 3]") == [1, 2, 3]

    def test_int(self):
        assert flexmod.auto_interpret("1") == 1

    def test_float(self):
        assert flexmod.auto_interpret("1.0") == 1.0

    def test_str(self):
        assert flexmod.auto_interpret("a") == "a"
    
    def test_bool(self):
        assert flexmod.auto_interpret("True") == True
        assert flexmod.auto_interpret("false") == False
        assert flexmod.auto_interpret("no") == False
        assert flexmod.auto_interpret("ON") == True

    def test_none(self):
        assert flexmod.auto_interpret(None) == None


class TestConfigValue:
    def test_basic(self):
        config_value = config_value_example_num_apples()
        try:
            config_value.value = "1"
            raise ValueError("Expected config value validation to fail.")
        except AssertionError:
            config_value.value = 1
            assert 1 == config_value.value


class TestAutolockedConfigValue:
    def test_basic(self):
        config_value = config_value_example_num_apples()
        config_value.value = 1
        assert not config_value.locked
        _ = config_value.value
        assert config_value.locked


class TestConfig:
    def test_basic(self):
        config_value = config_value_example_num_apples()
        config = Config("stats", [config_value])
        config["num_apples"] = 1
        try:
            _ = config["num_apples"]
            config["num_apples"] = 2
            raise ValueError("Expected config value to be locked.")
        except AssertionError:
            pass

    def test_raise_error_on_duplicate_name(self):
        config_value_a = config_value_example_num_apples()
        config_value_b = config_value_example_num_apples()
        try:
            _ = Config("stats", [config_value_a, config_value_b])
            raise Exception("Expected duplicate config value name to raise error.")
        except AssertionError:
            pass


class TestConfigIndex:
    def test_basic(self):
        config_value = config_value_example_num_apples()
        config = Config("stats", [config_value])
        config_index = ConfigIndex([config])
        hint_a = config_index.hint()
        
        config_index.load_override(os.path.join(DIR_PATH, "example.ini"))
        hint_b = config_index.hint()
        assert hint_a == hint_b
        assert config_index["stats"]["num_apples"] == 1
        try:
            config["num_apples"] = 2
            raise ValueError("Expected config value to be locked.")
        except AssertionError:
            pass
    
    def test_raise_error_on_duplicate_name(self):
        config_value_a = config_value_example_num_apples("num_apples_a")
        config_value_b = config_value_example_num_apples("num_apples_b")
        config_a = Config("stats", [config_value_a])
        config_b = Config("stats", [config_value_b])
        try:
            _ = ConfigIndex([config_a, config_b])
            raise Exception("Expected duplicate config name to raise error.")
        except AssertionError:
            pass