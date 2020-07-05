'''
----------------------------------------------------------------------------------------------------
airco_bedroom.py - handle AC related processing, including turning on/off based on door sensors.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
# from core.log import logging
import configuration
reload(configuration)
# from configuration import LOG_PREFIX
from core.actions import NotificationAction
from core.date import ZonedDateTime,minutes_between
from core.utils import iround

lastTime = ZonedDateTime.now()

#===================================================================================================
@rule("AC Bedroom Handling", description="Turn on or off AC in Bedroom based on time and temperature", tags=["astro"])
@when("Item AC_Temp_Bedroom changed")
@when("Item Alarm_Door_Bedroom changed")
@when("Time cron 0 */10 * * * ?")
@when("System started")
def aircoBedroom(event):
    global lastTime
    nowTime = ZonedDateTime.now()
    # Define threshold values
    tempNightThreshold = 18
    tempMorningThreshold = 19
    tempDayThreshold = 20
    tempThreshold = tempDayThreshold
    outsideTempHiThreshold = 23
    outsideTempLoThreshold = 14
    delay = 10                       # In minutes
    # Get current temperature readings
    tempBedroom = iround(float(str(items["AC_Temp_Bedroom"])))
    tempOutside = iround(float(str(items["AC_Temp_Outdoor"])))
    # Set status variables to default state
    doorIsOpen = False
    acIsOn = False
    # Set default state of the action variables
    turnOn = False
    turnOff = False
    warn = False
    msg = ""
    aircoBedroom.log.info(">>> Enter rule with inside temp [{}] and outside temp [{}]".format(tempBedroom, tempOutside))
    
    if ir.getItem("AC_Vacation_Bedroom").state != OFF:
        aircoBedroom.log.info("Vacation mode is on, exit Daikin rule")
        return

    # Check the current airco on/off status
    if not isinstance(ir.getItem("AC_Power_Bedroom"), UnDefType) and items["AC_Power_Bedroom"] == ON:
        acIsOn = True
        aircoBedroom.log.info("01. Airco is currently ON")
    # Check if the door is open
    if not isinstance(ir.getItem("AC_Power_Bedroom"), UnDefType) and items["Alarm_Door_Bedroom"] == OPEN:
        doorIsOpen = True
        aircoBedroom.log.info("02. Door currently OPEN")
        turnOff = True
    # Check if day or evening/night/morning
    if nowTime.hour >= 19 or nowTime.hour <= 6:
        tempThreshold = tempNightThreshold
    elif nowTime.hour <= 7:
        tempThreshold = tempMorningThreshold
    else:
        tempThreshold = tempDayThreshold
    aircoBedroom.log.info("03. Inside temp threshold of [{}] used".format(tempThreshold))
    # Turn on the airco if it is very hot outside, regardless of time of day or bedroom temperature 
    if tempOutside > outsideTempHiThreshold:
        if not acIsOn:
            msg = "It is hot outside, so I turned on the airco in the bedroom for you to keep it cool"
            turnOn = True
        aircoBedroom.log.info("04. Outside temp above [{}], set turn-AC-on flag [{}]".format(tempOutside, turnOn))
    else:
        if ir.getItem("AC_Vacation_Bedroom").state == ON:
            aircoBedroom.log.info("Vacation mode is on, turn off AC and exit Daikin rule")
            events.sendCommand("AC_Power_Bedroom", "OFF")
            return

        # Check if bedroom temperature is above threshold to turn AC on
        if tempBedroom > tempThreshold:
            msg = "The bedroom temperature is rising, so I turned on the airco to keep it cool"
            turnOn = True
            aircoBedroom.log.info("05. Bedroom temp [{}] > [{}], turn-AC-on flag is set to [{}]".format(tempBedroom, tempThreshold, turnOn))
        else:
            # If bedroom is cooled off, check if outside is cool as well
            if tempOutside < outsideTempLoThreshold:
                msg = "The bedroom is cool now, so I turned off the airco for you"
                turnOn = False
                turnOff = True
                aircoBedroom.log.info("06. Bedroom temp is [{}], turn-AC-on flag set to [{}]".format(tempBedroom, turnOn))
            else:
                aircoBedroom.log.info("07.Bedroom temp [{}] below threshold, but outside temp [{}], not turning off the AC if still on, AC-on is [{}]".format(tempBedroom, tempOutside, acIsOn))

    # Turn off the Airco if the door is open
    if doorIsOpen:
        if turnOn:
            msg = "The bedroom temperature is rising, but I cannot turn on the airco because the door is open. Please close the door first."
            warn = True
            turnOn = False
            turnOff = True
            aircoBedroom.log.info("08. The door is open and Turn-AC-On flag is set; set warn flag to [{}]".format(warn))
        if acIsOn:
            events.sendCommand("AC_Power_Bedroom", "OFF")
            lastTime = nowTime
            acIsOn = False
            turnOn = False
            msg = "The bedroom airco is on but the door is open. I turned off the airco for you. Please, close the door."
            warn = True
            aircoBedroom.log.info("09. AC is on and door is open, turn off the AC")
    # How long ago did we change the status (to prevent flapping)
    duration = int(str(minutes_between(lastTime, ZonedDateTime.now())))
    aircoBedroom.log.info("Compare times, last time [{}], now [{}], diff [{}]".format(lastTime, nowTime, duration))
    if duration > delay:
        aircoBedroom.log.info("10. Check turn on/off change because more than [{}] seconds have passed since last check".format(delay))
        if turnOn:
            if not acIsOn:
                aircoBedroom.log.info("Turn on the AC")
                events.sendCommand("AC_Power_Bedroom", "ON")
                lastTime = ZonedDateTime.now()
                # acIsOn = True
            else:
                msg = ""
                aircoBedroom.log.info("11. AC already on, ignoring turn on action")
        else:
            if acIsOn and turnOff:
                aircoBedroom.log.info("Turn off the AC")
                events.sendCommand("AC_Power_Bedroom", "OFF")
                lastTime = ZonedDateTime.now()
                acIsOn = False
            else:
                msg = ""
                aircoBedroom.log.info("12. AC already off, ignoring turn off action")
    else:
        msg = ""
        aircoBedroom.log.info("13. Last update no more than [{}] minutes ago, ignoring change".format(duration))
    # Set and report (new) airco state.
    if msg != "" and acIsOn != turnOn:
        NotificationAction.sendBroadcastNotification(msg)
        aircoBedroom.log.info(msg)
        if items["AC_MessageRepeat"] != ON:
            aircoBedroom.log.info("Sending message [{}] to Alexa".format(msg))
            if warn:
                msg = "WARNING! " + msg
            else:
                msg = "Hi, " + msg
            # Echo_TTS_Livingroom.sendCommand(msg)
            events.sendCommand("AC_MessageRepeat", "ON")
            lastTime = ZonedDateTime.now()
            acIsOn = False
        else:
            aircoBedroom.log.info("14. Skipping message [{}] to Alexa".format(msg))
    else:
        aircoBedroom.log.info("15. Airco on state is [{}], desired turn on state [{}]".format(acIsOn, turnOn))
