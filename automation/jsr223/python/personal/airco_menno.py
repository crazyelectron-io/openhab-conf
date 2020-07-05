'''
----------------------------------------------------------------------------------------------------
airco_menno.py - Check the mode of the AC
----------------------------------------------------------------------------------------------------
Changelog:
20200705 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
# from core.log import logging
import configuration
reload(configuration)

#==================================================================================================
@rule("AC Guestroom Handling", description="Set mode of AC in Guestroom if not Cooling", tags=["airco"])
@when("Time cron 0 */5 * * * ?")
@when("System started")
def aircoGuestroom(event):
    aircoGuestroom.log.info(">>> Enter rule")

    if not isinstance(ir.getItem("AC_Power_Guestroom"), UnDefType) and items["AC_Power_Guestroom"] == ON:
        aircoGuestroom.log.info("01. Airco Guestroom is ON, set Mode to COLD and Fan to AUTO")
        events.sendCommand("AC_Mode_Guestroom", "COLD")
        events.sendCommand("AC_FanSpeed_Guestroom", "AUTO")
