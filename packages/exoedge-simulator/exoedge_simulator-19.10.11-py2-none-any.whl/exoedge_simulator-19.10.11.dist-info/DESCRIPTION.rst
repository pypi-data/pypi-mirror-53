Description
############

This project is a Simulator source for Exosite's ``ExoSense`` which uses ``ExoEdge``

Install
#########

Installing a build can be done in several ways:

Installing From Source
"""""""""""""""""""""""

.. code-block:: bash

    $ python setup.py install


Installing From Builds
"""""""""""""""""""""""

.. code-block:: bash

    $ pip install dist/*.whl


Installing From Builds
"""""""""""""""""""""""

.. code-block:: bash

    $ pip install exoedge_simulator



ExoSense Configuration
########################

Below is an example config\_io that works for generating a sin_wave

.. code-block:: json

    {
      "channels": {
        "000": {
          "channel_name": "000",
          "description": "Sin Wave",
          "display_name": "Sin Wave",
          "properties": {
            "data_type": "TEMPERATURE",
            "data_unit": "DEG_FAHRENHEIT",
            "device_diagnostic": false,
            "max": null,
            "min": null,
            "precision": 2
          },
          "protocol_config": {
            "app_specific_config": {
              "function": "sin_wave",
              "parameters": {
                "amplitude": 1,
                "offset": 0,
                "period": 60,
                "precision": 2
              }
            },
            "application": "Simulator",
            "down_sample": "actual",
            "input_raw": {},
            "interface": null,
            "report_on_change": false,
            "report_rate": 10000,
            "sample_rate": 10000,
            "timeout": null
          }
        }
      }
    }

Available Functions
"""""""""""""""""""

The following are functions supported by the simulator, including their parameters with defaults.
Additional parameters can be included, and will be ignored.

**fourteen**

Returns 14

.. code-block:: json

    "function": "fourteen",
    "parameters": {}


**current_time**

Returns the current timestamp

.. code-block:: json

    "function": "current_time",
    "parameters": {}


**echo**

Echo a value into a string

.. code-block:: json

    "function": "echo",
    "parameters": {
        "value": "Hello World"
    }


**strip\_non\_numeric**

Strip out non-numeric characters from string

.. code-block:: json

    "function": "strip_non_numeric",
    "parameters": {
        "value": "1234BEEF"
    }


**sin_wave**

Generate a sin wave from the current time

.. code-block:: json

    "function": "sin_wave",
    "parameters": {
        "period": 60,
        "amplitude": 1,
        "offset": 0,
        "precision": 2
    }


**cos_wave**

Generate a cos wave from the current time

.. code-block:: json

    "function": "cos_wave",
    "parameters": {
        "period": 60,
        "amplitude": 1,
        "offset": 0,
        "precision": 2
    }


**location**

Generate location data from the current time and a starting location

Moves in a circle every `period` seconds. Path is `radius` decimal degrees
from the center point defined by `latitude` and `longitude`.

.. code-block:: json

    "function": "location",
    "parameters": {
        "latitude": None,
        "longitude": None,
        "period": 60,
        "radius": 0.1,
        "precision": 6
    }


**random_integer**

Get a random integer between two values

.. code-block:: json

    "function": "random_integer",
    "parameters": {
        "lower": 0,
        "upper": 10
    }


**random_sleep**

Sleep for a random number of seconds

.. code-block:: json

    "function": "random_sleep",
    "parameters": {
        "lower": 0,
        "upper": 10
    }


**ip_address**

Returns a string that represents the ip address in octet form of the iface parameter given.
    Parameters:
        interface: The network interface. Use `ifconfig` (MAC, linux) or `ipconfig` (Windows) to check the interface.


.. code-block:: json

    "function": "ip_address",
    "parameters": {
        "interface":"en0"
    }

return something like: {"000": ["192.168.2.143"]}


