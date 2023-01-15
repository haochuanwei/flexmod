# flexmod
A python module for other modules to allow flexible (yet not error-prone) configuration.

## Usage

Define configurations in your module using flexmod classes:

```python
# mypackage/__init__.py
from flexmod import AutolockedConfigValue, AutolockedConfig, AutolockedConfigIndex

config = AutolockedConfigIndex(
    [
        AutolockedConfig(
	    "interface",
	    [
	    	AutolockedConfigValue(
		    # name of the config paramater
		    "language",
		    # hint
		    "The language of module interface (logs, warnings, etc.)",
		    # default value
		    "en-us",
		),
	    	AutolockedConfigValue(
		    "verbosity",
		    "The granularity to which the module reports / complains",
		    1,
		    # specify a preprocessing function if needed
		    preprocessing=int,
		    # validate the config value
		    validation=lambda x: (isinstance(x, int) and x >= 0),
		),
	    ],
	),
        AutolockedConfig(
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

Your user can use `load_override` to customize your module:
```
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


