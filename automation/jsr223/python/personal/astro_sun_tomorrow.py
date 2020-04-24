'''
----------------------------------------------------------------------------------------------------
astro_sun_tomorrow.py - Calculate tomorrows sunrise and sunset times.
----------------------------------------------------------------------------------------------------
Changelog:
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.items import add_item
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX, COUNTRY, LATITUDE, LONGITUDE, CITY
from org.joda.time import DateTime
import datetime

#---------------------------------------------------------------------------------------------------
# create Sunrise and Sunset Items if they do not exist
def addSunriseItems():
    addSunriseItems.log = logging.getLogger("{}.addSunriseItems".format(LOG_PREFIX))
    # scriptExtension.importPreset("RuleSupport")
    try:
        if ir.getItems("Astro_Sun_SetTomorrow") == []:
            add_item("Astro_Sun_SetTomorrow", item_type="DateTime", groups=["gAstro"], label="Tomorrow's Sunset [%1$tH:%1$tM]", category="sunset", tags=["Astro"])
        if ir.getItems("Astro_Sun_RiseTomorrow") == []:
            add_item("Astro_Sun_RiseTomorrow", item_type="DateTime", groups=["gAstro"], label="Tomorrow's Sunrise [%1$tH:%1$tM]", category="sunrise", tags=["Astro"])
        if ir.getItems("Astro_Sun_SetNext") == []:
            add_item("Astro_Sun_SetNext", item_type="DateTime", groups=["gAstro"], label="Zonsondergang [%1$tH:%1$tM]", category="sunset", tags=["Astro"])
        if ir.getItems("Astro_Sun_RiseNext") == []:
            add_item("Astro_Sun_RiseNext", item_type="DateTime", groups=["gAstro"], label="Zonsopkomst [%1$tH:%1$tM]", category="sunrise", tags=["Astro"])
    except:
        import traceback
        addSunriseItems.log.error(traceback.format_exc())

#---------------------------------------------------------------------------------------------------
# Use this to remove created items. For testing purposes only!
def removeSunriseItems():
    from core.items import remove_item
    remove_item("Astro_Sun_SetTomorrow")
    remove_item("Astro_Sun_RiseTomorrow")
    remove_item("Astro_Sun_SetNext")
    remove_item("Astro_Sun_RiseNext")

#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    # removeSunriseItems()
    addSunriseItems()

#---------------------------------------------------------------------------------------------------
def calcNextSunTimes():
    calcNextSunTimes.log = logging.getLogger("{}.calcNextSunTimes".format(LOG_PREFIX))
    if str(items["Astro_Day_Phase"]) in ["DAYLIGHT", "NOON"]:
        calcNextSunTimes.log.info("Daylight - next sunrise is tomorrow, next sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTomorrow").state))
        events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTime").state))
    elif str(ir.getItem("Astro_Day_Phase").state) == "SUN_RISE":
        calcNextSunTimes.log.info("Sunrise - next sunrise and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTime").state))
        events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTime").state))
    elif str(ir.getItem("Astro_Day_Phase").state) == "SUN_SET":
        calcNextSunTimes.log.info("Sunset - next sunrise is tomorrow and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTomorrow").state))
        events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTime").state))
    elif str(ir.getItem("Astro_Day_Phase").state) in ["ASTRO_DAWN", "NAUTIC_DAWN", "CIVIL_DAWN"]:
        calcNextSunTimes.log.info("Dawn - next sunrise and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTime").state))
        events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTime").state))
    elif str(ir.getItem("Astro_Day_Phase").state) in ["ASTRO_DUSK", "NAUTIC_DUSK", "CIVIL_DUSK"]:
        calcNextSunTimes.log.info("Dusk - next sunrise and sunset is tomorrow")
        events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTomorrow").state))
        events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTomorrow").state))
    else:
        if DateTime.now().getHourOfDay() > 12:
            calcNextSunTimes.log.info("Before midnight - next sunrise and sunset is tomorrow")
            events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTomorrow").state))
            events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTomorrow").state))
        else:
            calcNextSunTimes.log.info("After midnight - next sunrise and sunset is today")
            events.postUpdate("Astro_Sun_RiseNext", str(ir.getItem("Astro_Sun_RiseTime").state))
            events.postUpdate("Astro_Sun_SetNext", str(ir.getItem("Astro_Sun_SetTime").state))


#===================================================================================================
@rule("AstroNextSun", description="Determine the next sunrise/sunset times for today and tomorrow", tags=["astro"])
@when("Item Astro_Day_Phase changed")
def astroNextSunTimes(event):
    calcNextSunTimes()


#===================================================================================================
@rule("AstroSunTomorrow", description="Calculate tomorrow's sunrise/sunset time", tags=["astro"])
@when("Time cron 0 10 0 ? * * *")
@when("System started")
def calcSunTomorrow(event):
    import astral # pylint: disable=import-error
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    my = astral.Location(info=(CITY, COUNTRY, LATITUDE, LONGITUDE, "Europe/Amsterdam", 1))
    my.solar_depression = 'civil'
    sun = my.sun(date=tomorrow, local=True)
    events.postUpdate("Astro_Sun_RiseTomorrow", str(sun['sunrise'].isoformat())[11:16])
    events.postUpdate("Astro_Sun_SetTomorrow", str(sun['sunset'].isoformat())[11:16])
    calcSunTomorrow.log.info("Tomorrow's sunrise [{}] and sunset [{}] calculated".format(str(sun['sunrise'].isoformat())[11:16], str(sun['sunset'].isoformat())[11:16]))
    calcNextSunTimes()