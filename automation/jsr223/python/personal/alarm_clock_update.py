'''
----------------------------------------------------------------------------------------------------
alarm_clock_update.py - 
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
from core.date import to_joda_datetime
from org.joda.time import DateTime

timerAlarm = None

#==================================================================================================
@rule("Alarm Clock Update", description="Take morning actions when the Android Alarm goes off", tags=["alarm"])
@when("Item AlarmClock changed")
def alarmClockUpdate(event):
    global timerAlarm

    if event.oldItemState is None:
        return

    alarmClockUpdate.log = logging.getLogger("{}.alarmClockUpdate".format(LOG_PREFIX))

    if ir.getItem("AlarmClock").state == 0:
        alarmClockUpdate.log.info("AlarmClock state changed to 0, cancel all alarms")
        if timerAlarm is not None and not timerAlarm.hasTerminated():
            alarmClockUpdate.log.info("AlarmClock timerAlarm is running, cancel it")
            timerAlarm.cancel()
    else:
        alarmClockUpdate.log.info("Schedule Android alarm for {}".format(ir.getItem("AlarmClock").state) )
        if timerAlarm is not None and not timerAlarm.hasTerminated():
            alarmClockUpdate.log.info("Reschedule Android alarm to {}".format(ir.getItem("AlarmClock").state) )
            timerAlarm.cancel()
        else:
            alarmClockUpdate.log.info("New Android Alarm set for [{}]".format(ir.getItem("AlarmClock").state) )
            timerAlarm = ScriptExecution.createTimer(to_joda_datetime(event.itemState), lambda: events.sendCommand("Light_Scene_Hall","EVENING"))