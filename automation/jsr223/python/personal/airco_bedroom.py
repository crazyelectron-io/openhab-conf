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
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX
from core.actions import NotificationAction
from core.date import ZonedDateTime,minutes_between
from core.utils import iround

lastTime = ZonedDateTime.now()

#==================================================================================================
@rule("AC Bedroom Handling", description="Turn on or off AC in Bedroom based on time and temperature", tags=["astro"])
@when("Item AC_Temp_Bedroom changed")
@when("Item Alarm_Door_Bedroom changed")
@when("Time cron 0 */10 * * * ?")
@when("System started")
def aircoBedroom(event):
    global lastTime

    aircoBedroom.log = logging.getLogger("{}.aircoBedroom".format(LOG_PREFIX))

    nowTime = ZonedDateTime.now()

    # Define threshold values
    tempNightThreshold = 17
    tempMorningThreshold = 18
    tempDayThreshold = 21
    tempThreshold = tempDayThreshold
    outsideTempHiThreshold = 25
    outsideTempLoThreshold = 17
    delay = 8 # In minutes

    # Get current temperature readings
    # tempBedroom = iround(float(str(ir.getItem("AC_Temp_Bedroom").state)))
    tempBedroom = iround(float(str(items["AC_Temp_Bedroom"])))
    # tempOutside = iround(float(str(ir.getItem("AC_Temp_Outdoor").state)))
    tempOutside = iround(float(str(items["AC_Temp_Outdoor"])))

    # Set status variables to default state
    doorIsOpen = False
    acIsOn = False

    # Set default state of the action variables
    turnOn = False
    turnOff = False
    warn = False
    msg = ""

    aircoBedroom.log.debug(">>> Enter rule with inside temp [{}] and outside temp [{}]".format(tempBedroom, tempOutside))

    # Check the current airco on/off status
    if not isinstance(ir.getItem("AC_Power_Bedroom"), UnDefType) and ir.getItem("AC_Power_Bedroom").state == ON:
        acIsOn = True
        aircoBedroom.log.debug("01. Airco is currently ON")

    # Check if the door is open
    if not isinstance(ir.getItem("AC_Power_Bedroom"), UnDefType) and ir.getItem("Alarm_Door_Bedroom").state == OPEN:
        doorIsOpen = True
        aircoBedroom.log.debug("02. Door currently OPEN")
        turnOff = True

    # Check if day or evening/night/morning
    if nowTime.hour >= 19 or nowTime.hour <= 6:
        tempThreshold = tempNightThreshold
    elif nowTime.hour <= 7:
        tempThreshold = tempMorningThreshold
    else:
        tempThreshold = tempDayThreshold
    aircoBedroom.log.debug("03. Inside temp threshold of [{}] used".format(tempThreshold))

    # Turn on the airco if it is very hot outside, regardless of time of day or bedroom temperature 
    if tempOutside > outsideTempHiThreshold:
        if not acIsOn:
            msg = "It is hot outside, so I turned on the airco in the bedroom for you to keep it cool"
            turnOn = True
        aircoBedroom.log.debug("04. Outside temp above [{}], set turn-AC-on flag [{}]".format(tempOutside, turnOn))
    else:
        if ir.getItem("AC_Vacation_Bedroom").state == ON:
            aircoBedroom.log.debug("Vacation mode is on, turn off AC and exit Daikin rule")
            events.sendCommand("AC_Power_Bedroom", "OFF")
            return

        # Check if bedroom temperature is above threshold to turn AC on
        if tempBedroom > tempThreshold:
            msg = "The bedroom temperature is rising, so I turned on the airco to keep it cool"
            turnOn = True
            aircoBedroom.log.debug("05. Bedroom temp [{}] > [{}], turn-AC-on flag is set to [{}]".format(tempBedroom, tempThreshold, turnOn))
        else:
            # If bedroom is cooled off, check if outside is cool as well
            if tempOutside < outsideTempLoThreshold:
                msg = "The bedroom is cool now, so I turned off the airco for you"
                turnOn = False
                turnOff = True
                aircoBedroom.log.debug("06. Bedroom temp is [{}], turn-AC-on flag set to [{}]".format(tempBedroom, turnOn))
            else:
                aircoBedroom.log.debug("07.Bedroom temp [{}] below threshold, but outside temp [{}], not turning off the AC if still on, AC-on is [{}]".format(tempBedroom, tempOutside, acIsOn))

    # Turn off the Airco if the door is open
    if doorIsOpen:
        if turnOn:
            msg = "The bedroom temperature is rising, but I cannot turn on the airco because the door is open. Please close the door first."
            warn = True
            turnOn = False
            turnOff = True
            aircoBedroom.log.debug("08. The door is open and Turn-AC-On flag is set; set warn flag to [{}]".format(warn))
        if acIsOn:
            events.sendCommand("AC_Power_Bedroom", "OFF")
            lastTime = nowTime
            acIsOn = False
            turnOn = False
            msg = "The bedroom airco is o n but the door is open. I turned off the airco for you. Please, close the door."
            warn = True
            aircoBedroom.log.debug("09. AC is on and door is open, turn off the AC")

    duration = int(str(minutes_between(lastTime, ZonedDateTime.now())))
    aircoBedroom.log.debug("Compare times, last time [{}], now [{}], diff [{}]".format(lastTime, nowTime, duration))

    if duration > delay:
        aircoBedroom.log.debug("10. Check turn on/off change because more than [{}] seconds have passed since last check".format(delay))
        if turnOn:
            if not acIsOn:
                aircoBedroom.log.info("Turn on the AC")
                events.sendCommand("AC_Power_Bedroom", "ON")
                lastTime = ZonedDateTime.now()
                # acIsOn = True
            else:
                msg = ""
                aircoBedroom.log.debug("11. AC already on, ignoring turn on action")
        else:
            if acIsOn and turnOff:
                aircoBedroom.log.info("Turn off the AC")
                events.sendCommand("AC_Power_Bedroom", "OFF")
                lastTime = ZonedDateTime.now()
                acIsOn = False
            else:
                msg = ""
                aircoBedroom.log.debug("12. AC already off, ignoring turn off action")
    else:
        msg = ""
        aircoBedroom.log.debug("13. Last update no more than [{}] minutes ago, ignoring change".format(duration))

    if msg != "" and acIsOn != turnOn:
        NotificationAction.sendBroadcastNotification(msg)
        aircoBedroom.log.debug(msg)
        if ir.getItem("AC_MessageRepeat").state != ON:
            aircoBedroom.log.debug("Sending message [{}] to Alexa".format(msg))
            if warn:
                msg = "WARNING! " + msg
            else:
                msg = "Hi, " + msg
            # Echo_TTS_Livingroom.sendCommand(msg)
            events.sendCommand("AC_MessageRepeat", "ON")
            lastTime = ZonedDateTime.now()
            acIsOn = False
        else:
            aircoBedroom.log.debug("14. Skipping message [{}] to Alexa".format(msg))
    else:
        aircoBedroom.log.debug("15. Airco on state is [{}], desired turn on state [{}]".format(acIsOn, turnOn))
