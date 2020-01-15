'''
astro.rules - Astro related processing, including sun and moon data and day/night triggers.
----------------------------------------------------------------------------------------------------
v14 21091229 Changed extra logging to debug level.
v13 20191226 Merged tomorrow sunset/rise rules; fixed Item name 'Astro_Sun_Elevation'.
v12 20191222 Renamed Items.
v11 20191025 Added next day sunrise/sunset handling.
--------------------------------------------------------------------------------------------------
Rules in this file:
Astro.DayPhase - Calculate current day Mode and next sunrise/sunset times.
Astro_Sun.Position - Translate sun position to text (wind direction).
Astro.Sun.Tomorrow - Calculate tomorrow's sunrise and sunset time.
Alarm.Clock.Change - Android Alarm clock actions.
--------------------------------------------------------------------------------------------------
Items changes in these rules:
Day_Mode - MORNING, DAY, EVENING, NIGHT; based on time, sun and cloudiness.
Astro_Sun_Direction - Textual description of the wind direction of the sun position.
Astro_Sun_RiseTomorrow - Tomorrow's sunrise time, calculated with Python astral library (since
    the Astro binding only gives today's times). 
Astro_Sun_SetTomorrow - Tomorrow's sunset time, calculated with Python astral library.
Astro_Sun_RiseNext - The next sunrise time (either today or tomorrow).
Astro_Sun_SetNext - The next sunset time (either today or tomorrow).
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from org.slf4j import LoggerFactory
from configuration import LOG_PREFIX

# from core.jsr223 import scope
# from core.items import add_item
# from core.actions import HTTP
# from core.utils import postUpdate as post_update
# from datetime import datetime, timedelta

log = LoggerFactory.getLogger("{}.my.astro".format(LOG_PREFIX))

#==================================================================================================
# Update String Item Astro_Sun_Direction with textual representation of current sun angle.
#==================================================================================================
@rule("AstroSunPosition", description="Translate Sun Azimut to Wind Direction", tags=["astro"])
@when("Item Astro_Sun_Azimuth changed")
def update_sun_direction(event):
    log.info("Update textual Sun direction Item '{}' from Azumith [{}]", event.itemName, event.itemState)

    wind_directions = {
        range(0, 12) : 'North',
        range(12, 34) : 'North-NorthEast',
        range(34, 57) : 'North-East',
        range(57, 79) : 'East-NorthEast',
        range(79, 102) : 'East',
        range(102, 125) : 'East-SouthEast',
        range(125, 147) : 'SouthEast',
        range(147, 170) : 'South-SouthEast',
        range(170, 192) : 'South',
        range(192, 215) : 'South-SouthWest',
        range(215, 237) : 'SouthWest',
        range(237, 259) : 'West-SouthWest',
        range(259, 283) : 'West',
        range(283, 305) : 'West-NorthWest',
        range(305, 327) : 'NorthWest',
        range(327, 349) : 'North-NorthWest',
        range(349, 366) : 'North'
    }

    for key in wind_directions:
        if event.itemState in key:
            wind_direction = wind_directions[key]
            log.info("Wind direction translate is '{}', wind_direction)
            events.postUpdate("Astro_Sun_Direction", wind_direction)
            break


'''
#==================================================================================================
# Update the next sunset/rise times and Day Mode when the Astro day phase changes or the Cloudiness
#  changes.
#==================================================================================================
@rule("AstroDayPhase", description="Calculate current day Mode and next sunrise/sunset times", tags=["astro"])
@when("Item Astro_Day_Phase changed")
@when("Item Weather_Cloudy changed")
@when("System started")
def set_day_mode_and_sunset_rise_time(event):
    cloudy = false

    #---Sanity checks
    if ir.item("Astro_Day_Phase").state == NULL:
        return

    phase = Astro_Day_Phase.state.toString()
    hour = now.getHourOfDay()

    if ir.item("Weather_Cloudy").state != NULL and ir.item("Weather_Cloudy").state == "ON":
        log.info("Set Cloudy switch to True")
        cloudy = true

    #---Update Day Mode based on Astro Day Phase
    #   SUN_RISE, ASTRO_DAWN, NAUTIC_DAWN, CIVIL_DAWN, CIVIL_DUSK, NAUTIC_DUSK, ASTRO_DUSK, SUN_SET, DAYLIGHT, NIGHT
    switch (phase)
    {
        case "DAYLIGHT":
        {
            logDebug(TAG, "Day Phase is DAYLIGHT, check time to set Day Mode to MORNING or DAY")
            Day_Mode.sendCommand(if (hour>=7) "DAY" else "MORNING")
        }
        case "SUN_SET":
        {
            logDebug(TAG, "Day Phase is sunset, check if cloudy")
            Day_Mode.sendCommand(if (cloudy) "EVENING" else "DAY")
        }
        case "SUN_RISE":
        {
            logDebug(TAG, "Day Phase is sunrise, check if cloudy")
            Day_Mode.sendCommand(if (cloudy) "MORNING" else "DAY")
        }
        case "ASTRO_DAWN",
        case "NAUTIC_DAWN",
        case "CIVIL_DAWN":
        {
            logDebug(TAG, "Day Phase is DAWN")
            Day_Mode.sendCommand(if (hour >= 6) "MORNING" else "NIGHT")
        }
        case "ASTRO_DUSK",
        case "NAUTIC_DUST",
        case "CIVIL_DUSK":
        {
            logDebug(TAG, "Day Phase is DUSK")
            Day_Mode.sendCommand(if (hour<=23) "EVENING" else "NIGHT")
        }
        case "NIGHT":
        {
            logDebug(TAG, "Day Phase is NIGHT")
            Day_Mode.sendCommand(if (hour<=23) "EVENING" else "NIGHT")
        }
    }

    #---Determine next sunset/sunrise times for today and tomorrow.
    if phase == "DAYLIGHT":
        # Set today's sunset and tomorrow's sunrise time.
        log.info("Daylight; next sunrise is tomorrow at {}, next sunset is today at {}.".format(ir.item("Astro_Sun_RiseTomorrow").state, ir.item("Astro_Sun_SetTime").state))
        sendCommandIfDifferent(Day_Mode, "DAY")
        Astro_Sun_RiseNext.postUpdate(Astro_Sun_RiseTomorrow.state)
        Astro_Sun_SetNext.postUpdate(Astro_Sun_SetTime.state)
    else:
        # Set today's sunset and tomorrow's sunrise.
        if now.getHourOfDay > 12:
            log.info("Evening; next sunrise is tomorrow at {}, next sunset is tomorrow at {}.", Astro_Sun_RiseTomorrow.state, Astro_Sun_SetTomorrow.state)
            Astro_Sun_RiseNext.postUpdate(Astro_Sun_RiseTomorrow.state)
            Astro_Sun_SetNext.postUpdate(Astro_Sun_SetTomorrow.state)
        else:
            log.info("Morning; next sunrise is today at {}, next sunset is today at {}.", Astro_Sun_RiseTime.state, Astro_Sun_SetTime.state)
            Astro_Sun_RiseNext.postUpdate(Astro_Sun_RiseTime.state)
            Astro_Sun_SetNext.postUpdate(Astro_Sun_SetTime.state)


#==================================================================================================
# Calculate tomorrow's sunrise/sunset time using the python astral library (via script).
#==================================================================================================
@rule("AstroSunTomorrow", description="Astro.Sun.Tomorrow - Calculate tomorrow's sunrise and sunset time", tags=["astro"])
@when("System started")
@when("cron 0 10 0 ? * * *")
def astro_sun_tomorrow(event):
    #---Calculate tomorrow's sunrise time
    timeString = executeCommandLine("python /openhab/conf/scripts/sunrise_tomorrow.py", 5000)
    if ir.item("Astro_Sun_RiseTomorrow") !== null and ir.item["Astro_Sun_RiseTomorrow").state != NULL:
        log.info("Tomorrow's sunrise time: {}".format(timeString))
        Astro_Sun_RiseTomorrow.postUpdate(DateTimeType.valueOf(timeString))
    else:
        log.info("Astro_Sun_RiseTomorrow not yet initialized")

    #-- Calculate tomorrow's sunset time
    timeString = executeCommandLine("python /openhab/conf/scripts/sunset_tomorrow.py", 5000)
    if Astro_Sun_SetTomorrow !== null and Astro_Sun_SetTomorrow.state != NULL:
        log.info("Tomorrow's sunset time: {}".format(timeString))
        postUpdate("Astro_Sun_SetTomorrow", DateTimeType.valueOf(timeString))
    else:
        log.info("Astro_Sun_SetTomorrow not yet initialized")


#==================================================================================================
# Take morning actions when the Android Alarm goes off
#==================================================================================================
# @rule( "AlarmClock", description="Android Alarm clock actions", tags=["astro"])
@when("Item AlarmClock changed")
def alarm_clock_update(event):
    log.info(">>>>>> Enter rule with '{}' >>>>>>".format(AlarmClock))

    if ir.item("AlarmClock").state == 0:
        log.info(TAG, "AlarmClock state changed to 0, cancel all alarms")
        if timerAlarm !== null:
            #timerAlarm?.cancel
            log.info("AlarmClock timerAlarm is running, cancel it")
            timerAlarm.cancel
            timerAlarm = null
    else:
        epoch = new DateTime((AlarmClock.state).longValue)
        log.info("Schedule Android alarm for {}".format(epoch.toString))

        if timerAlarm !== null:
            log.info("Reschedule Android alarm to {}".format(epoch.toString))
            timerAlarm.reschedule(epoch)
        else:
            log.info("New Android Alarm set to {}".format(epoch.toString))
            timerAlarm = createTimer(epoch,
                [|
                    # Turn off the House Alarm and turn on the hallway lighting
                    sendCommandIfDifferent("Light_Scene_Hall", "EVENING")
                    sendCommand("Alarm_Status", "DISARMED")
                    log.info("Android AlarmClock expired, turn on hall light and disarm the alarm")
                ]
            )
'''
