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
from configuration import LOG_PREFIX,COUNTRY,LATITUDE,LONGITUDE,CITY
import datetime
from org.joda.time import DateTime
import astral # pylint: disable=import-error

log = logging.getLogger("{}.astro_nextsun".format(LOG_PREFIX))

#===================================================================================================
@rule("AstroNextSun", description="Determine the next sunrise/sunset times for today and tomorrow", tags=["astro"])
@when("Item Astro_Day_Phase changed")
@when("System started")
def set_next_sun_times(event):
    if str(items.Astro_Day_Phase) == "DAYLIGHT":
        log.info("Daylight - next sunrise is tomorrow, next sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) == "SUN_RISE":
        log.info("Sunrise - next sunrise and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTime))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) == "SUN_SET":
        log.info("Sunset - next sunrise is tomorrow and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) in ["ASTRO_DAWN", "NAUTIC_DAWN", "CIVIL_DAWN"]:
        log.info("Dawn - next sunrise and sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTime))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))
    elif str(items.Astro_Day_Phase) in ["ASTRO_DUSK", "NAUTIC_DUSK", "CIVIL_DUSK:
        log.info("Dusk - next sunrise and sunset is tomorrow")
        events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
        events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTomorrow))
    else:
        if DateTime.now().getHourOfDay() > 12:
            log.info("Before midnight - next sunrise and sunset is tomorrow")
            events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTomorrow))
            events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTomorrow))
        else:
            log.info("After midnight - next sunrise and sunset is today")
            events.postUpdate("Astro_Sun_RiseNext", str(items.Astro_Sun_RiseTime))
            events.postUpdate("Astro_Sun_SetNext", str(items.Astro_Sun_SetTime))


#===================================================================================================
@rule("AstroSunTomorrow", description="Calculate tomorrow's sunrise/sunset time", tags=["astro"])
@when("Time cron 0 10 0 ? * * *")
@when("System started")
def calc_sun_tomorrow(event):
    # Determine tomorrow's date
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    my = astral.Location(info=(CITY, COUNTRY, LATITUDE, LONGITUDE, "Europe/Amsterdam", 1))
    my.solar_depression = 'civil'
    sun = my.sun(date=tomorrow, local=True)

    events.postUpdate("Astro_Sun_RiseTomorrow", str(sun['sunrise'].isoformat())[11:16])
    events.postUpdate("Astro_Sun_SetTomorrow", str(sun['sunset'].isoformat())[11:16])
