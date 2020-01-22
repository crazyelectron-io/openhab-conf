'''
----------------------------------------------------------------------------------------------------
astro_day_mode.py - Set the day mode based on time, cloudiness and sunset/sunrise.
----------------------------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
from org.joda.time import DateTime

log = logging.getLogger("{}.astro_day".format(LOG_PREFIX))


# Astro day phase:
# SUN_RISE, ASTRO_DAWN, NAUTIC_DAWN, CIVIL_DAWN, CIVIL_DUSK, NAUTIC_DUSK, ASTRO_DUSK, SUN_SET, DAYLIGHT, NIGHT
dayPhaseDict = {
    "DAYLIGHT": {
        "mode": "time",
        "mode_time": 7,
        "before": "MORNING",
        "after": "DAY",
    },
    "SUN_SET": {
        "mode": "cloud",
        "before": "EVENING",
        "after": "DAY",
    },
    "SUN_RISE": {
        "mode": "cloud",
        "before": "MORNING",
        "after": "DAY",
    },
    "ASTRO_DAWN": {
        "mode": "time",
        "mode_time": 6,
        "before": "NIGHT",
        "after": "MORNING",
    },
    "NAUTIC_DAWN": {
        "mode": "time",
        "mode_time": 6,
        "before": "NIGHT",
        "after": "MORNING",
    },
    "CIVIL_DAWN": {
        "mode": "time",
        "mode_time": 6,
        "before": "NIGHT",
        "after": "MORNING",
    },
    "ASTRO_DUSK": {
        "mode": "time",
        "mode_time": 23,
        "before": "EVENING",
        "after": "NIGHT",
    },
    "NAUTIC_DUSK": {
        "mode": "time",
        "mode_time": 23,
        "before": "EVENING",
        "after": "NIGHT",
    },
    "CIVIL_DUSK": {
        "mode": "time",
        "mode_time": 23,
        "before": "EVENING",
        "after": "NIGHT",
    },
    'NIGHT': {
        "mode": "time",
        "mode_time": 23,
        "before": "EVENING",
        "after": "NIGHT",
    },
}


#==================================================================================================
# Update the Day Mode when the Astro day phase changes or the Cloudiness changes.
#==================================================================================================
@rule("AstroDayPhase", description="Calculate current Day Mode based on time, weather and sun position", tags=["astro"])
@when("Item Astro_Day_Phase changed")
@when("Item Weather_Cloudy changed")
@when("System started")
def set_day_mode(event):
    global dayPhaseDict

    log.info("Start update Day_Mode base on time, phase and cloudiness")
    #--- Define used variables
    hour = DateTime.now().getHourOfDay()
    cloudy = False
    before = False

    #--- Is it currently cloudy?
    if items["Weather_Cloudy"] != NULL and items["Weather_Cloudy"] == "ON":
        log.info("Set Cloudy switch to True")
        cloudy = True

    #--- Update Day Mode based on Astro Day Phase, time and/or cloudiness
    keyItem = dayPhaseDict.get(str(items["Astro_Day_Phase"]))
    if keyItem.get("mode") == "time":
        keyTime = keyItem.get("mode_time")
        if keyTime < 12:
            before = True if hour <= keyTime else False
        else:
            before = True if hour >= keyTime else False
    else:
        before = cloudy

    events.postUpdateIfDifferent("Day_Mode", str(keyItem.get("before")) if before else str(keyItem.get("after")))
