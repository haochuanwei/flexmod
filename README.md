# flexmod
A python module for other modules to allow flexible (yet not error-prone) configuration.

## Story

Suppose you wrote a package and you want to allow users to set package-level configs:

```python
import awesomepackage
from awesomepackage.foo import bar

# user can change module param on the fly
awesomepackage.config["logging"]["verbose"] = True

# package behavior is now different from default
bar()
```

This is simple, but maybe not any parameter can be changed at any time. For example:

```python
awesomepackage.config["metric"]["length"] = "foot"
```

Having flexible units may be helpful for different locales, but changing metric units in the middle of a program can lead to consistency issues.

`flexmod` lets you:
-   specify configs that are auto-locked (i.e. no further changes) when used
-   add custom preprocessor functions to entered config values
    -   this is useful when reading config from a text file
-   add validation functions to check user-supplied config values

## Usage

### Define configurations in your module using `flexmod` classes

```python
# mypackage/__init__.py
from flexmod import ConfigValue, AutolockedConfigValue, Config, ConfigIndex

config = ConfigIndex(
    [
        Config(
	    "interface",
	    [
	        # example of a config that stays the same throughout a program
	    	AutolockedConfigValue(
		    # name of the config paramater
		    "language",
		    # hint
		    "The language of module interface (logs, warnings, etc.)",
		    # default value
		    "en-us",
		    # validate the config value
		    validation=lambda x: x in ["en-us", "fr-fr"],
		),
	        # example of a config that can change dynamically
	    	ConfigValue(
		    "verbosity",
		    "The granularity to which the module reports / complains",
		    1,
		    # specify a preprocessor function if needed
		    preprocessor=int,
		),
	    ],
	),
        Config(
	    "foo",
	    [
	    	AutolockedConfigValue(
		    "bar",
		    "Any other config parameter",
		    "",
		),
	    ],
	),
    ]
)
```

```python
# mypackage/message.py
import mypackage

def hello_world():
    """
    Example function that uses a module-level config.
    """
    lang = mypackage.config["interface"]["language"]
    if lang == "en-us":
        print("Hello, world!")
    elif lang == "fr-fr":
        print("Bonjour, tout le monde!")
    else:
        pass
```

### Package user: customize your module on the fly

Your user will not need to be aware of `flexmod`.

```python
import mypackage
from mypackage.message import hello_world

# change module param on the fly
mypackage.config["interface"]["language"] = "fr-fr"

# this gets "Bonjour, tout le monde!"
hello_world()

# after an autolocked config is read, it cannot be changed
mypackage.config["interface"]["language"] = "en-us"
# AssertionError: language is locked from updates.
```

Users can also supply an [configparser](https://docs.python.org/3/library/configparser.html)-style ini file.

-   Unlike in default configparser, booleans, integers and floats will be autodetected and converted.

```ini
# in custom.ini
[interface]
language = fr-fr
verbosity = 2

[foo]
bar = anything
```

```python
import mypackage
from mypackage.message import hello_world

# change module param on the fly
mypackage.config.load_override("custom.ini")

# this gets "Bonjour, tout le monde!"
hello_world()
```

