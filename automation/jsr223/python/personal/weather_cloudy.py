'''
----------------------------------------------------------------------------------------------------
weather_cloudy.py - Set global variable based on clioudiness.
----------------------------------------------------------------------------------------------------
Changelog:
20200119 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX

log = logging.getLogger("{}.weather_cloudy".format(LOG_PREFIX))

cloudyConditions = ["bewolkt", "zwaarbewolkt", "regen", "mist", "hagel", "sneeuw", "nachtmist", "wolkennacht"]

#===================================================================================================
@rule("WeatherCloudy", description="Determine Cloudiness of weather condition and set global variable", tags=["weather"])
@when("Item Weather_Condition changed")
def set_cloudy_state(event):
    weather = str(items.Weather_Condition)
    if weather in cloudyConditions:
        log.debug("Cloudy conditions, set Cloudy item")
        events.postUpdate("Weather_Cloudy", "ON")
    else:
        log.debug("Clear conditions, reset Cloudy item")
        events.postUpdate("Weather_Cloudy", "OFF")
