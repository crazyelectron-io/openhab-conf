'''
----------------------------------------------------------------------------------------------------
airco_menno.py - Check the mode of the AC
----------------------------------------------------------------------------------------------------
Changelog:
20200724 v02    Added SetTemp command.
20200705 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
import configuration
reload(configuration)
from core.utils import iround


tempGuestroom = iround(float(str(items["AC_Temp_Guestroom"])))

#==================================================================================================
@rule("AC Guestroom Handling", description="Set mode of AC in Guestroom if not Cooling", tags=["airco"])
@when("Time cron 0 */5 * * * ?")
@when("System started")
def aircoGuestroom(event):
    aircoGuestroom.log.info("00. >>> Enter rule")
    global tempGuestroom

    # if not isinstance(ir.getItem("AC_Timer_Guestroom"), UnDefType) and items["AC_Timer_Guestroom"] == OFF:
    #     aircoGuestroom.log.info("02. Night mode is OFF, check temperature")
    #     if tempGuestroom > 19:
    #         aircoGuestroom.log.info("03. Temp Guestroom is above minimum, turn on airco")
    #         events.sendCommand("AC_Power_Guestroom", "ON")
    #         events.sendCommand("AC_Mode_Guestroom", "COLD")
    #         events.sendCommand("AC_FanSpeed_Guestroom", "AUTO")
    #         events.sendCommand("AC_SetTemp_Guestroom", "18")
    #     else:
    #         aircoGuestroom.log.info("05. Temp Guestroom is below minimum, dont turn on airco")
    # else:
    #     aircoGuestroom.log.info("01. NightMode is on")

    if not isinstance(ir.getItem("AC_Power_Guestroom"), UnDefType) and items["AC_Power_Guestroom"] == ON:
        aircoGuestroom.log.info("04. Airco Guestroom is ON, set Mode to COLD and Fan to AUTO")
        events.sendCommand("AC_Mode_Guestroom", "COLD")
        events.sendCommand("AC_FanSpeed_Guestroom", "AUTO")
        events.sendCommand("AC_SetTemp_Guestroom", "18")

    aircoGuestroom.log.info("99. >>> Exit rule")


#==================================================================================================
@rule("AC Guestroom NightMode", description="Set Night Mode for 2 hour delay", tags=["airco"])
@when("Item AC_Timer_Guestroom received command ON")
def aircoGuestroomNightOn(event):
    aircoGuestroomNightOn.log.info("00. >>> Enter rule")

    if not isinstance(ir.getItem("AC_Power_Guestroom"), UnDefType) and items["AC_Power_Guestroom"] == ON:
        aircoGuestroomNightOn.log.info("01. Airco Guestroom is ON, turn off the airco and start timer")
        events.sendCommand("AC_Power_Guestroom", "OFF")

    aircoGuestroomNightOn.log.info("99. >>> Exit rule")


#==================================================================================================
@rule("AC Guestroom NightMode", description="Reset Night Mode after delay", tags=["airco"])
@when("Item AC_Timer_Guestroom received command OFF")
def aircoGuestroomNightOff(event):
    aircoGuestroomNightOff.log.info("00. >>> Enter NightMode ended rule")
    # global tempGuestroom

    if not isinstance(ir.getItem("AC_Power_Guestroom"), UnDefType) and items["AC_Power_Guestroom"] == OFF:
        aircoGuestroomNightOff.log.info("01. NightMode Timer OFF, check temperature")
        # if tempGuestroom > 18:
        aircoGuestroomNightOff.log.info("02. Temp Guestroom is above minimum, turn on airco")
        # events.sendCommand("AC_Power_Guestroom", "ON")
