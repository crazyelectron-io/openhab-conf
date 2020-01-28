'''
----------------------------------------------------------------------------------------------------
weather_avg_outdoor.py - Set avg outdoor temperature based on temp around house and weather station.
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
from configuration import LOG_PREFIX

log = logging.getLogger("{}.astro_nextsun".format(LOG_PREFIX))

#===================================================================================================
@rule("WeatherAvgOutdoorTemp", description="Set avg outdoor temperature based on temp around house and weather station", tags=["weather"])
@when("Item AC_Temp_Outdoor changed")
@when("Item Weather_Temp_WeatherStation changed")
def weather_avg_outdoor(event):
    #--- Calc average of two measurements if available, else use just one value.
    if items.Weather_Temp_WeatherStation is not None:
        if items.AC_Temp_Outdoor is not None:
            events.postUpdate( "Weather_TempAverage_Outdoor", str((float(str(items.Weather_Temp_WeatherStation)) + float(str(items.AC_Temp_Outdoor)))/2))
        else:
            events.postUpdate("Weather_TempAverage_Outdoor", str(items.Weather_Temp_WeatherStation))
            log.info("Daikin outdoor temp sensor data not initialized, using weather station data only")
    elif items.AC_Temp_Outdoor is not None:
        events.postUpdate("Weather_TempAverage_Outdoor", str(items.AC_Temp_Outdoor))
        log.info("Weather station temp not initialized, using Daikin outdoor temp sensor data only")
    else:
        log.info("Both outdoor temperature values are NULL, skipping average calculation")
