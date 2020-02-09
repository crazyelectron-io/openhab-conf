'''
----------------------------------------------------------------------------------------------------
alarm_status_update.py - Handle alarm status update trigger.
----------------------------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
# from core.log import logging
# import configuration
# reload(configuration)
# from configuration import LOG_PREFIX
from core.actions import NotificationAction

#===================================================================================================
@rule("Alarm Status Update", description="Alarm status has changed, report it via Alexa and Push notification", tags=["alarm"])
@when("Item Alarm_Status changed")
def alarmStatusUpdate(event):
    if event.oldItemState is None:
        return
    alarmStatusUpdate.log.info("Alarm changed from [{}] to [{}]".format(event.oldItemState, event.itemState))
    state = "Armed" if items["Alarm_Status"] == StringType("ARMED_AWAY") or \
        items["Alarm_Status"] == StringType("ARMED_HOME") else "Disarmed"
    # Echo_TTS_Livingroom.sendCommand("<speak>Hi, " + msg + "</speak>")
    NotificationAction.sendBroadcastNotification("The alarm has been " + state)