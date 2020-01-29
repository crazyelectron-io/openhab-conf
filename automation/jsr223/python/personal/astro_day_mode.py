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
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX, DAY_PHASES_DICT


#---------------------------------------------------------------------------------------------------
# create Day Mode Item if it does not exist
def addDayModeItem():
    addDayModeItem.log = logging.getLogger("{}.addDayModeItem".format(LOG_PREFIX))

    scriptExtension.importPreset("RuleSupport")

    from core.items import add_item

    try:
        if ir.getItems("Day_Mode") == []:
            add_item("Day_Mode", item_type="String", groups=["gAstro,gPersist"], label="Current day mode [%s]", category="sunset", tags=["Astro"])
    except:
        import traceback
        addDayModeItem.log.error(traceback.format_exc())


#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    addDayModeItem()


#==================================================================================================
@rule("AstroDayPhase", description="Update current Day Mode based on time, weather and sun position", tags=["astro"])
@when("Item Astro_Day_Phase changed")
@when("Item Weather_Cloudy changed")
@when("Item Alarm_Status changed to ARMED_HOME")
@when("Item Alarm_Status changed to ARMED_AWAY")
@when("System started")
def setDayMode(event):
    setDayMode.log = logging.getLogger("{}.setDayMode".format(LOG_PREFIX))

    cloudy = str(items.Weather_Cloudy) or "OFF"

    from org.joda.time import DateTime

    keyItem = DAY_PHASES_DICT.get(str(items.Astro_Day_Phase))
    if keyItem.get("mode") == "time":
        newState = keyItem.get("before_state") if DateTime.now().getHourOfDay() <= keyItem.get("mode_time") else keyItem.get("after_state")
    else:
        newState = keyItem.get("clear_state") if cloudy == "OFF" else keyItem.get("cloudy_state")

    setDayMode.log.info("Set Day_Mode to [{}], if different from [{}]".format(newState, items.Day_Mode))

    from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent

    postUpdateCheckFirst("Day_Mode", str(newState))
