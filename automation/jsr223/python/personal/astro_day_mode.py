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
from configuration import LOG_PREFIX,DAY_PHASES_DICT
from org.joda.time import DateTime

log = logging.getLogger("{}.astro_day".format(LOG_PREFIX))


#==================================================================================================
@rule("AstroDayPhase", description="Update current Day Mode based on time, weather and sun position", tags=["astro"])
@when("Item Astro_Day_Phase changed")
@when("Item Weather_Cloudy changed")
@when("System started")
def set_day_mode(event):
    log.info("Start update Day_Mode base on time, phase and cloudiness")

    #--- Is it currently cloudy?
    cloudy = items["Weather_Cloudy"] or "OFF"
    log.info("Cloudy state is {}".format(cloudy))

    #--- Update Day Mode based on Astro Day Phase, time and/or cloudiness
    keyItem = DAY_PHASES_DICT.get(str(items["Astro_Day_Phase"]))
    if keyItem.get("mode") == "time":
        phaseTime = keyItem.get("mode_time")
        if phaseTime < 12:
            before = "before" if DateTime.now().getHourOfDay()<=phaseTime else "after"
        else:
            before = "before" if DateTime.now().getHourOfDay()>=phaseTime else "after"
    else:
        before = "before" if cloudy=="ON" else "after"

    log.info("Set Day_Mode to {} = {}".format(before, str(keyItem.get(before))))
    events.postUpdate("Day_Mode", str(keyItem.get(before)))
