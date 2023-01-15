"""
Simple tests.
"""
import os
import flexmod
from flexmod import ConfigValue, AutolockedConfigValue, AutolockedConfig, AutolockedConfigIndex

DIR_PATH = os.path.dirname(__file__)

class Dummy:
    def __init__(self, value):
        self.value = value

class TestConfigValue:
    def test_basic(self):
        config_value = ConfigValue("num_apples", "number of apples", preprocessor=lambda x: x, validation=lambda x: isinstance(x, int), default=0)
        try:
            config_value.value = "1"
            raise ValueError("Expected config value validation to fail.")
        except AssertionError:
            config_value.value = 1
            assert not config_value.locked
            _ = config_value.value
            assert not config_value.locked

class TestAutolockedConfigValue:
    def test_basic(self):
        config_value = AutolockedConfigValue("num_apples", "number of apples", preprocessor=lambda x: x, validation=lambda x: isinstance(x, int), default=0)
        config_value.value = 1
        assert not config_value.locked
        _ = config_value.value
        assert config_value.locked

class TestAutolockedConfig:
    def test_basic(self):
        config_value = AutolockedConfigValue("num_apples", "number of apples", preprocessor=lambda x: x, validation=lambda x: isinstance(x, int), default=0)
        config = AutolockedConfig("stats", [config_value])
        config["num_apples"] = 1
        try:
            _ = config["num_apples"]
            config["num_apples"] = 2
            raise ValueError("Expected config value to be locked.")
        except AssertionError:
            pass

class TestAutolockedConfigIndex:
    def test_basic(self):
        config_value = AutolockedConfigValue("num_apples", "number of apples", preprocessor=lambda x: x, validation=lambda x: isinstance(x, int), default=0)
        config = AutolockedConfig("stats", [config_value])
        config_index = AutolockedConfigIndex([config])
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
