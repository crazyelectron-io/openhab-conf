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
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX, COUNTRY, LATITUDE, LONGITUDE, CITY


#---------------------------------------------------------------------------------------------------
# create Sunrise and Sunset Items if they do not exist
def addSunriseItems():
    addSunriseItems.log = logging.getLogger("{}.addSunriseItems".format(LOG_PREFIX))

    scriptExtension.importPreset("RuleSupport")

    from core.items import add_item

    try:
        if ir.getItems("Astro_Sun_SetTomorrow") == []:
            add_item("Astro_Sun_SetTomorrow", item_type="DateTime", groups=["gAstro"], label="Tomorrow's Sunset [%1$tH:%1$tMs]", category="sunset", tags=["Astro"])
        if ir.getItems("Astro_Sun_RiseTomorrow") == []:
            add_item("Astro_Sun_RiseTomorrow", item_type="DateTime", groups=["gAstro"], label="Tomorrow's Sunrise [%1$tH:%1$tMs]", category="sunrise", tags=["Astro"])
        if ir.getItems("Astro_Sun_SetNext") == []:
            add_item("Astro_Sun_SetNext", item_type="DateTime", groups=["gAstro"], label="Next Sunset [%1$tH:%1$tMs]", category="sunset", tags=["Astro"])
        if ir.getItems("Astro_Sun_RiseNext") == []:
            add_item("Astro_Sun_RiseNext", item_type="DateTime", groups=["gAstro"], label="Next Sunrise [%1$tH:%1$tMs]", category="sunrise", tags=["Astro"])
    except:
        import traceback
        addSunriseItems.log.error(traceback.format_exc())


#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    addSunriseItems()


#---------------------------------------------------------------------------------------------------
def calcNextSunTimes():
    calcNextSunTimes.log = logging.getLogger("{}.calcNextSunTimes".format(LOG_PREFIX))

    if str(items.Astro_Day_Phase) == "DAYLIGHT":
        calcNextSunTimes.log.info("Daylight - next sunrise is tomorrow, next sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) == "SUN_RISE":
        calcNextSunTimes.log.info("Sunrise - next sunrise and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTime))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) == "SUN_SET":
        calcNextSunTimes.log.info("Sunset - next sunrise is tomorrow and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) in ["ASTRO_DAWN", "NAUTIC_DAWN", "CIVIL_DAWN"]:
        calcNextSunTimes.log.info("Dawn - next sunrise and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTime))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) in ["ASTRO_DUSK", "NAUTIC_DUSK", "CIVIL_DUSK"]:
        calcNextSunTimes.log.info("Dusk - next sunrise and sunset is tomorrow")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTomorrow))
    else:
        from org.joda.time import DateTime

        if DateTime.now().getHourOfDay() > 12:
            calcNextSunTimes.log.info("Before midnight - next sunrise and sunset is tomorrow")
            events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
            events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTomorrow))
        else:
            calcNextSunTimes.log.info("After midnight - next sunrise and sunset is today")
            events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTime))
            events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))


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
    calcSunTomorrow.log = logging.getLogger("{}.addSunriseItems".format(LOG_PREFIX))

    import astral # pylint: disable=import-error
    import datetime

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    my = astral.Location(info=(CITY, COUNTRY, LATITUDE, LONGITUDE, "Europe/Amsterdam", 1))
    my.solar_depression = 'civil'
    sun = my.sun(date=tomorrow, local=True)

    events.postUpdate("Astro_Sun_RiseTomorrow", str(sun['sunrise'].isoformat())[11:16])
    events.postUpdate("Astro_Sun_SetTomorrow", str(sun['sunset'].isoformat())[11:16])
    calcSunTomorrow.log.info("Tomorrow's sunrise [{}] and sunset [{}] calculated".format(str(sun['sunrise'].isoformat())[11:16], str(sun['sunset'].isoformat())[11:16]))

    calcNextSunTimes()