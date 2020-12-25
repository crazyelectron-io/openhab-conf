'''
----------------------------------------------------------------------------------------------------
airco_bedroom.py - handle AC related processing, including turning on/off based on door sensors.
----------------------------------------------------------------------------------------------------
Changelog:
20200704 v02    Updated with fan mode/speed settings.
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
import configuration
reload(configuration)
from core.actions import NotificationAction
from core.date import ZonedDateTime,minutes_between
from core.utils import iround


#===================================================================================================
@rule("AC Bedroom Handling", description="Turn on or off AC in Bedroom based on time and temperature", tags=["astro"])
@when("Item Alarm_Door_Bedroom changed")
@when("Time cron 0 */10 * * * ?")
@when("System started")
def aircoBedroom(event):
    #--- Define threshold values
    tempNightThreshold = 18
    tempMorningThreshold = 19
    tempDayThreshold = 20
    tempThreshold = tempDayThreshold
    outsideTempHiThreshold = 23
    outsideTempLoThreshold = 16
    #--- Get current temperature readings
    tempBedroom = iround(float(str(items["AC_Temp_Bedroom"])))
    tempOutside = iround(float(str(items["AC_Temp_Outdoor"])))
    #--- Set status variables to default state
    doorIsOpen = False
    #--- Set default state of the action variables
    turnOn = 0
    msg = ""
    aircoBedroom.log.info(">>> Enter rule with inside temp [{}] and outside temp [{}] >>>".format(tempBedroom, tempOutside))
    
    if not isinstance(ir.getItem("AC_Vacation_Bedroom"), UnDefType) and ir.getItem("AC_Vacation_Bedroom").state == ON:
        aircoBedroom.log.info("00. Vacation mode is on, exit Daikin rule")
        return

    #--- Check the current airco on/off status
    if not isinstance(ir.getItem("AC_Power_Bedroom"), UnDefType) and items["AC_Power_Bedroom"] == ON:
        aircoBedroom.log.debug("01. Airco is currently ON")
    # Check if the door is open
    if not isinstance(ir.getItem("Alarm_Door_Bedroom"), UnDefType) and items["Alarm_Door_Bedroom"] == OPEN:
        doorIsOpen = True
        aircoBedroom.log.info("02. Door currently OPEN")
        turnOn = -1
    # Check if day or evening/night/morning
    if ZonedDateTime.now().hour >= 18 or ZonedDateTime.now().hour <= 6:
        tempThreshold = tempNightThreshold
    elif ZonedDateTime.now().hour <= 7:
        tempThreshold = tempMorningThreshold
    else:
        tempThreshold = tempDayThreshold
    aircoBedroom.log.debug("03. Inside temp threshold of [{}] used".format(tempThreshold))
    # Turn on the airco if it is very hot outside, regardless of time of day or bedroom temperature 
    if tempOutside > outsideTempHiThreshold:
        if items["AC_Power_Bedroom"] != ON:
            msg = "It is hot outside, so I turned on the airco in the bedroom for you to keep it cool"
            turnOn = 1
        aircoBedroom.log.debug("04. Outside temp above [{}], set turn-AC-on flag [{}]".format(tempOutside, turnOn))

    # Check if bedroom temperature is above threshold to turn AC on
    if tempBedroom > tempThreshold:
        msg = "The bedroom temperature is rising, so I turned on the airco to keep it cool"
        turnOn = 1
        aircoBedroom.log.debug("06. Bedroom temp [{}] > [{}], turn-AC-on flag is set to [{}]".format(tempBedroom, tempThreshold, turnOn))
    else:
        # If bedroom is cooled off, check if outside is cool as well
        if tempOutside < outsideTempLoThreshold:
            msg = "The bedroom is cool now, so I turned off the airco for you"
            turnOn = -1
            aircoBedroom.log.debug("07. Bedroom temp is [{}], turn-AC-on flag set to [{}]".format(tempBedroom, turnOn))
        else:
            aircoBedroom.log.debug("08. Bedroom temp [{}] below threshold, but outside temp [{}] above threshold, not turning off the AC if still on, AC status is [{}]".format(tempBedroom, tempOutside, items["AC_Power_Bedroom"] == ON))

    #--- Turn off the Airco if the door is open
    if doorIsOpen:
        if turnOn == 1:
            msg = "The bedroom temperature is rising, but I cannot turn on the airco because the door is open. Please close the door first."
            turnOn = -1
            aircoBedroom.log.debug("09. The door is open and Turn-AC-On flag is set")
        if items["AC_Power_Bedroom"] == ON:
            events.sendCommand("AC_Power_Bedroom", "OFF")
            turnOn = 0
            msg = "The bedroom airco is on but the door is open. I turned off the airco for you. Please, close the door."
            aircoBedroom.log.info("10. AC is on and door is open, turn off the AC")

    if turnOn == 1:
        if items["AC_Power_Bedroom"] != ON:
            aircoBedroom.log.info("11. Turn on the AC")
            events.sendCommand("AC_Power_Bedroom", "ON")
            events.sendCommand("AC_Mode_Bedroom", "COLD")
            events.sendCommand("AC_SetTemp_Bedroom", "18")
            if tempOutside > outsideTempLoThreshold:
                events.sendCommand("AC_FanSpeed_Bedroom", "AUTO")
            else:
                events.sendCommand("AC_FanSpeed_Bedroom", "SILENT")
        else:
            msg = ""
            aircoBedroom.log.debug("12. AC already on, ignoring turn on action")
    elif turnOn == -1:
        if items["AC_Power_Bedroom"] == ON:
            aircoBedroom.log.info("13. Turn off the AC")
            events.sendCommand("AC_Power_Bedroom", "OFF")
        else:
            msg = ""
            aircoBedroom.log.debug("14. AC already off, ignoring turn off action")

    #--- Set and report (new) airco state.
    if msg != "":
        if (turnOn and items["AC_Power_Bedroom"] != ON) or (not turnOn and items["AC_Power_Bedroom"] == ON):    #acIsOn != turnOn:
            NotificationAction.sendBroadcastNotification(msg)
            aircoBedroom.log.info(msg)
            if items["AC_MessageRepeat"] != ON:
                aircoBedroom.log.debug("15. Sending message [{}] to Alexa".format(msg))
                # Echo_TTS_Livingroom.sendCommand(msg)
                events.sendCommand("AC_MessageRepeat", "ON")
            else:
                aircoBedroom.log.debug("16. Skipping message [{}] to Alexa".format(msg))
    else:
        aircoBedroom.log.debug("17. Airco on state is [{}], desired turn on state [{}]".format(items["AC_Power_Bedroom"] == ON, turnOn))
