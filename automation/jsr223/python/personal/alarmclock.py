'''
----------------------------------------------------------------------------------------------------
alarmclock.py - 
----------------------------------------------------------------------------------------------------
Changelog:
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
from core.actions import ScriptExecution

log = logging.getLogger("{}.alarmclock".format(LOG_PREFIX))

timerAlarm = None

#==================================================================================================
@rule("AlarmClock", description="Take morning actions when the Android Alarm goes off", tags=["alarm"])
@when("Item AlarmClock changed")
def alarm_clock_update(event):
    global timerAlarm

    if items.AlarmClock == 0:
        log.info("AlarmClock state changed to 0, cancel all alarms")
        if timerAlarm is not None and not timerAlarm.hasTerminated():
            log.info("AlarmClock timerAlarm is running, cancel it")
            timerAlarm.cancel()
    else:
        log.info("Schedule Android alarm for {}".format(items.AlarmClock))
        if timerAlarm is not None and not timerAlarm.hasTerminated():
            log.info("Reschedule Android alarm to {}".format(items.AlarmClock))
            timerAlarm.cancel()
        else:
            log.info("New Android Alarm set for [{}]".format(items.AlarmClock))
            timerAlarm = ScriptExecution.createTimer(event.itemState, lambda: events.sendCommand("Light_Scene_Hall","EVENING"))
