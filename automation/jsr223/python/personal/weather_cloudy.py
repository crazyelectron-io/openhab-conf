'''
----------------------------------------------------------------------------------------------------
weather_cloudy.py - Set global variable based on clioudiness.
----------------------------------------------------------------------------------------------------
Changelog:
20200226 v02    Added 'buien' to cloudy conditions.
20200119 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when


cloudyConditions = ["bewolkt", "zwaarbewolkt", "regen", "buien", "mist", "hagel", "sneeuw", "nachtmist", "wolkennacht"]


#===================================================================================================
@rule("Weather Cloudy State", description="Determine Cloudiness of weather condition and set global variable", tags=["weather"])
@when("Item Weather_Condition changed")
def setCloudyState(event):
    weather = str(items["Weather_Condition"])
    if weather in cloudyConditions:
        setCloudyState.log.debug("Cloudy conditions, set Cloudy item")
        events.postUpdate("Weather_Cloudy", "ON")
    else:
        setCloudyState.log.debug("Clear conditions, reset Cloudy item")
        events.postUpdate("Weather_Cloudy", "OFF")
