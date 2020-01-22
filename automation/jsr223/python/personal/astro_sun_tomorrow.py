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
import astral    # pylint: disable=import-error


log = logging.getLogger("{}.astro_sun".format(LOG_PREFIX))


#===================================================================================================
# Determine next sunset/sunrise times for today and tomorrow.
#===================================================================================================
@rule("AstroNextSun", description="Calculate next sunrise/sunset time", tags=["astro"])
@when("Item Astro_Day_Phase changed")
@when("Item Weather_Cloudy changed")
@when("System started")
def set_next_sun_times(event):
    if items["Astro_Day_Phase"] == "DAYLIGHT":
        # Set today's sunset and tomorrow's sunrise time.
        log.info("Daylight - next sunrise is tomorrow, next sunset is today")
        events.postUpdate("Astro_Sun_RiseNext", items["Astro_Sun_RiseTomorrow"])
        events.postUpdate("Astro_Sun_SetNext", items["Astro_Sun_SetTime"])
    else:
        # Set today's sunset and tomorrow's sunrise.
        if str(DateTime.now().getHourOfDay()) > 12:
            log.info("Evening - next sunrise and sunset is tomorrow")
            events.postUpdate("Astro_Sun_RiseNext", items["Astro_Sun_RiseTomorrow"].toString())
            events.postUpdate("Astro_Sun_SetNext", items["Astro_Sun_SetTomorrow"].toString())
        else:
            log.info("Morning - next sunrise and sunset is today")
            events.postUpdate("Astro_Sun_RiseNext", items["Astro_Sun_RiseTime"].toString())
            events.postUpdate("Astro_Sun_SetNext", items["Astro_Sun_SetTime"].toString())


#===================================================================================================
# Calculate tomorrow's sunrise/sunset time using the python astral library
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
