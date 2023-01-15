"""
Toolbox for your library to be dynamically configured by the user.
Add defaults, hints, locks, preprocessors and validations for robustness.
"""
import re
import configparser
from typing import Any, Callable, List
from collections import defaultdict


def auto_interpret(text):
    """
    Automatic interpretation of a string.
    """
    if not isinstance(text, str):
        return text

    if re.search(r"^\-?\d+$", text):
        return int(text)
    if re.search(r"^\-?\d+\.\d+$", text):
        return float(text)
    if re.search(r"(?i)^(yes|on|true)$", text):
        return True
    if re.search(r"(?i)^(no|off|false)$", text):
        return False
    return text

class ConfigValue:
    """
    Base class not intended to be used directly.
    """
    def __init__(
        self,
        name: str,
        hint: str,
        preprocessor: Callable,
        validation: Callable,
        default: Any,
    ):
        self.name = name
        self.hint = hint
        self._preprocessor = preprocessor
        self._validation = validation
        self._example = default
        self._value = self.parse(default)
        self._value_lock = False

    def parse(self, value):
        value = self._preprocessor(value)
        assert self._validation(
            value
        ), f"Validation failed.\nHint: {self.hint}\nExample: {self.example}"
        return value

    @property
    def example(self):
        """
        An example raw (not preprocessed) value.
        """
        return self._example

    @property
    def value(self):
        """
        Reading the value can trigger something (lock) in subclasses.
        """
        return self._value

    @value.setter
    def value(self, value):
        assert not self.locked, f"{self.name} is locked from updates."
        self._value = self.parse(value)

    @property
    def locked(self):
        return self._value_lock

    
class AutolockedConfigValue(ConfigValue):
    """
    Config that locks it self upon a value read operation.
    """
    @property
    def value(self):
        """
        A value that, once read, no longer takes assignment.
        """
        self._value_lock = True
        return self._value

    @value.setter
    def value(self, value):
        assert not self.locked, f"{self.name} is locked from updates."
        self._value = self.parse(value)


class AutolockedConfig:
    """
    Dict-like object where key reads locks the value from updates.
    """

    def __init__(
        self,
        name: str,
        values: List[AutolockedConfigValue],
    ):
        self.name = name
        self._data = dict()
        for _value in values:
            assert isinstance(_value, AutolockedConfigValue)
            self._data[_value.name] = _value

    def __getitem__(self, key):
        return self._data[key].value

    def __setitem__(self, key, value):
        self._data[key].value = value

    def update(self, data_dict):
        """
        Check all the key lock statuses, then update.
        """
        for _k in data_dict.keys():
            assert not self._data[_k].locked, f"{_k} is locked from updates."
        for _k, _v in data_dict.items():
            self[_k] = _v

    def hint(self):
        return {
            _k: f"{_v.hint}. Example: {_v.example}" for _k, _v in self._data.items()
        }

    def items(self):
        return {_k: _v.value for _k, _v in self._data.items()}


class AutolockedConfigIndex:
    """
    ConfigParser-like object where sub-dictionaries are AutolockedConfig's.
    """

    def __init__(
        self,
        configs: List[AutolockedConfig],
    ):
        self._configs = dict()
        self._value_name_to_config_names = defaultdict(list)
        for _config in configs:
            # assign configs
            assert isinstance(_config, AutolockedConfig)
            self._configs[_config.name] = _config

    def __getitem__(self, key):
        return self._configs[key]

    def load_override(self, ini_path):
        parser = configparser.ConfigParser()
        parser.read(ini_path)

        for _section in parser.sections():
            assert _section in self._configs, f"Unexpected section {_section}"
            _dict = {_k: auto_interpret(_v) for _k, _v in parser[_section].items()}
            self._configs[_section].update(_dict)

    def hint(self):
        return {_k: _v.hint() for _k, _v in self._configs.items()}
