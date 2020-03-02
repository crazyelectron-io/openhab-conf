'''
--------------------------------------------------------------------------------
set_day_mode.py - Set the day mode based on time, cloudiness and sunset/sunrise.
--------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
--------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
from core.items import add_item
from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent
from org.joda.time import DateTime
import configuration
reload(configuration)
from configuration import LOG_PREFIX, DAY_PHASES_DICT


#-------------------------------------------------------------------------------
# create Day_Mode Item if it does not exist
def addDayModeItem():
    addDayModeItem.log = logging.getLogger("{}.addDayModeItem".format(LOG_PREFIX))
    # scriptExtension.importPreset("RuleSupport")

    try:
        if ir.getItems("Day_Mode") == []:
            add_item("Day_Mode",
                item_type="String",
                groups=["gAstro,gPersist"],
                label="Current day mode [%s]",
                category="sunset",
                tags=["Astro"]
            )
    except:
        import traceback
        addDayModeItem.log.error(traceback.format_exc())


#-------------------------------------------------------------------------------
def scriptLoaded(id):
    addDayModeItem()


#===============================================================================
@rule("Astro Set Day Mode",
    description="Update current Day Mode based on time, weather and sun position",
    tags=["astro"]
)
@when("Item Astro_Day_Phase changed")
@when("Item Weather_Cloudy changed")
@when("Item Alarm_Status changed to ARMED_HOME")
@when("Item Alarm_Status changed to ARMED_AWAY")
# @when("Time cron 0 */10 * * * ?")
@when("System started")
def setDayMode(event):
    # setDayMode.log = logging.getLogger("{}.setDayMode".format(LOG_PREFIX))
    setDayMode.log.info(
        "Enter Day_Mode with Day_Mode [{}], Clouds [{}], Astro_Day_Phase [{}]".format(
            ir.getItem("Day_Mode").state,
            ir.getItem("Weather_Cloudy").state,
            ir.getItem("Astro_Day_Phase").state
        )
    )

    cloudy = str(ir.getItem("Weather_Cloudy").state)  or "OFF"

    keyItem = DAY_PHASES_DICT.get(str(ir.getItem("Astro_Day_Phase").state) )
    setDayMode.log.info("Day Phase entry is [{}]".format(keyItem.get("mode")))

    if keyItem.get("mode") == "time":
        if DateTime.now().getHourOfDay() < keyItem.get("mode_time"):
            newState = keyItem.get("before_state")
        else:
            newState = keyItem.get("after_state")
        # TODO: Fix this hack:
        if str(ir.getItem("Astro_Day_Phase").state) in ["NIGHT", "NAUTIC_DAWN", "CIVIL_DAWN", "ASTRO_DAWN"] and DateTime.now().getHourOfDay() <= 6:
            newState = "NIGHT"
    else:
        newState = keyItem.get("clear_state") if cloudy == "OFF" else keyItem.get("cloudy_state")

    setDayMode.log.info("Set Day_Mode to [{}], if different from [{}]".format(newState, ir.getItem("Day_Mode").state))
    postUpdateCheckFirst("Day_Mode", str(newState))
