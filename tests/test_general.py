"""
Simple tests.
"""
import os
import flexmod
from flexmod import ConfigValue, AutolockedConfigValue, Config, ConfigIndex

DIR_PATH = os.path.dirname(__file__)

class Dummy:
    def __init__(self, value):
        self.value = value

class TestConfigValue:
    def test_basic(self):
        config_value = ConfigValue("num_apples", "number of apples", 0, preprocessor=lambda x: x, validation=lambda x: isinstance(x, int))
        try:
            config_value.value = "1"
            raise ValueError("Expected config value validation to fail.")
        except AssertionError:
            config_value.value = 1
            assert 1 == config_value.value

class TestAutolockedConfigValue:
    def test_basic(self):
        config_value = AutolockedConfigValue("num_apples", "number of apples", 0, preprocessor=lambda x: x, validation=lambda x: isinstance(x, int))
        config_value.value = 1
        assert not config_value.locked
        _ = config_value.value
        assert config_value.locked

class TestConfig:
    def test_basic(self):
        config_value = AutolockedConfigValue("num_apples", "number of apples", 0, preprocessor=lambda x: x, validation=lambda x: isinstance(x, int))
        config = Config("stats", [config_value])
        config["num_apples"] = 1
        try:
            _ = config["num_apples"]
            config["num_apples"] = 2
            raise ValueError("Expected config value to be locked.")
        except AssertionError:
            pass

class TestConfigIndex:
    def test_basic(self):
        config_value = AutolockedConfigValue("num_apples", "number of apples", 0, preprocessor=lambda x: x, validation=lambda x: isinstance(x, int))
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
