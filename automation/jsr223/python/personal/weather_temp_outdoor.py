'''
----------------------------------------------------------------------------------------------------
weather_temp_outdoor.py - Set average outdoor temperature based on multiple measurements.
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

#===================================================================================================
# @rule("WeatherTempOutdoor", description="Set average outdoor temperature based on measured temperature around house and weather station.", tags=["weather"])
# @when("Item AC_Temp_Outdoor changed")
# @when("Item Weather_Temp_WeatherStation changed")
# def weather_temp_outdoor(event):
#     log.info("Enter with {name}".format(name='event.itemNames")

#     #--- Calc average of two measurements if available, else use just one value.
#     if (Weather_Temp_WeatherStation.state != NULL) {
#         if (AC_Temp_Outdoor.state != NULL)
#         {
#             Weather_TempAverage_Outdoor.postUpdate(String::format("%.1f", ((Weather_Temp_WeatherStation.state as Number) + (AC_Temp_Outdoor.state as Number))/2))
#         }
#         else {
#             Weather_TempAverage_Outdoor.postUpdate(String::format("%.1f", Weather_Temp_WeatherStation.state as Number))
#             logDebug(TAG, "Daikin outdoor temp sensor data not initialized, using weather station data only")
#         }
#     }
#     else if (AC_Temp_Outdoor.state != NULL) { 
#         Weather_TempAverage_Outdoor.postUpdate(String::format("%.1f", AC_Temp_Outdoor.state as Number))
#         logDebug(TAG, "Weather station temp not initialized, using Daikin outdoor temp sensor data only")
#     }
#     else
#     {
#         logInfo(TAG, "Both outdoor temperature values are NULL, skipping average calculation")
#     }

#     logDebug(TAG, "<<<<<< Exit rule <<<<<<")
# end
