'''
----------------------------------------------------------------------------------------------------
astro_sun_direction.py - Translate Sun azimuth to wind direction.
----------------------------------------------------------------------------------------------------
Changelog:
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when


#==================================================================================================
# Update String Item Astro_Sun_Direction with textual representation of current sun angle.
#==================================================================================================
@rule("AstroSunPosition", description="Translate Sun Azimut degrees to Wind Direction", tags=["astro"])
@when("Item Astro_Sun_Azimuth changed")
def update_sun_direction(event):
    wind_directions = {
        xrange(0, 12) : 'North',
        xrange(12, 34) : 'North-NorthEast',
        xrange(34, 57) : 'North-East',
        xrange(57, 79) : 'East-NorthEast',
        xrange(79, 102) : 'East',
        xrange(102, 125) : 'East-SouthEast',
        xrange(125, 147) : 'SouthEast',
        xrange(147, 170) : 'South-SouthEast',
        xrange(170, 192) : 'South',
        xrange(192, 215) : 'South-SouthWest',
        xrange(215, 237) : 'SouthWest',
        xrange(237, 259) : 'West-SouthWest',
        xrange(259, 283) : 'West',
        xrange(283, 305) : 'West-NorthWest',
        xrange(305, 327) : 'NorthWest',
        xrange(327, 349) : 'North-NorthWest',
        xrange(349, 366) : 'North'
    }

    azimuth = int(float(str(event.itemState)))
    for key in wind_directions:
        # log.info("Wind direction translation table key [{}]", key)
        if azimuth in key:
            wind_direction = wind_directions[key]
            events.postUpdate("Astro_Sun_Direction", wind_direction)
            break


# #==================================================================================================
# # Take morning actions when the Android Alarm goes off
# #==================================================================================================
# # @rule( "AlarmClock", description="Android Alarm clock actions", tags=["astro"])
# @when("Item AlarmClock changed")
# def alarm_clock_update(event):
#     log.info(">>>>>> Enter rule with '{}' >>>>>>".format(AlarmClock))

#     if ir.item("AlarmClock").state == 0:
#         log.info(TAG, "AlarmClock state changed to 0, cancel all alarms")
#         if timerAlarm !== null:
#             #timerAlarm?.cancel
#             log.info("AlarmClock timerAlarm is running, cancel it")
#             timerAlarm.cancel
#             timerAlarm = null
#     else:
#         epoch = new DateTime((AlarmClock.state).longValue)
#         log.info("Schedule Android alarm for {}".format(epoch.toString))

#         if timerAlarm !== null:
#             log.info("Reschedule Android alarm to {}".format(epoch.toString))
#             timerAlarm.reschedule(epoch)
#         else:
#             log.info("New Android Alarm set to {}".format(epoch.toString))
#             timerAlarm = createTimer(epoch,
#                 [|
#                     # Turn off the House Alarm and turn on the hallway lighting
#                     sendCommandIfDifferent("Light_Scene_Hall", "EVENING")
#                     sendCommand("Alarm_Status", "DISARMED")
#                     log.info("Android AlarmClock expired, turn on hall light and disarm the alarm")
#                 ]
#             )
# '''
