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

#===================================================================================================
@rule("Weather Outdoor Temp", description="Set avg outdoor temperature based on temp around house and weather station", tags=["weather"])
@when("Item AC_Temp_Outdoor changed")
@when("Item Weather_Temp_WeatherStation changed")
def weatherOutdoorTemp(event):
    #--- Calc average of two measurements if available, else use just one value.
    if not isinstance(ir.getItem("Weather_Temp_WeatherStation"), UnDefType):
        if not isinstance(ir.getItem("AC_Temp_Outdoor"), UnDefType):
            events.postUpdate( "Weather_TempAverage_Outdoor", str((float(str(items["Weather_Temp_WeatherStation"])) + float(str(items["AC_Temp_Outdoor"])))/2))
        else:
            events.postUpdate("Weather_TempAverage_Outdoor", str(items["Weather_Temp_WeatherStation"]))
            weatherOutdoorTemp.log.info("Daikin outdoor temp sensor data not initialized, using weather station data only")
    elif not isinstance(ir.getItem("AC_Temp_Outdoor"), UnDefType):
        events.postUpdate("Weather_TempAverage_Outdoor", str(items["AC_Temp_Outdoor"]))
        weatherOutdoorTemp.log.info("Weather station temp not initialized, using Daikin outdoor temp sensor data only")
    else:
        weatherOutdoorTemp.log.warn("Both outdoor temperature values are NULL, skipping average calculation")
