'''
----------------------------------------------------------------------------------------------------
alarm.py - Handle alarm change commands and trigger other actions.
----------------------------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX
from core.actions import NotificationAction


log = logging.getLogger("{}.verisure".format(LOG_PREFIX))


#===================================================================================================
@rule("AlarmStatus", description="Alarm status has changed, report it via Echo Dot and push notification", tags=["alarm"])
@when("Item Alarm_Status changed")
def alarm_status_update(event):
    log.info("Alarm changed from [{}] to [{}]".format(event.oldItemState, event.itemState))
    if event.oldItemState is None:
        return
    state = "Armed" if str(items["Alarm_Status"]) == "ARMED_AWAY" or str(items["Alarm_Status"]) == "ARMED_HOME" else "Disarmed"
    # Echo_TTS_Livingroom.sendCommand("<speak>Hi, " + msg + "</speak>")
    NotificationAction.sendBroadcastNotification("The alarm has been " + state)


#===================================================================================================
@rule("AlarmTimeChange", description="The alarm status has changed, retrieve user and time of day summary", tags=["alarm"])
@when("Item Alarm_Time changed")
def alarm_time_update(event):
    summary = str(items["Alarm_User"]).split(' ')[0] + " at " + ((str(items["Alarm_Time.state"]).split('T')[1]).split('\\.')[0])[0:5] + " via " + str(items["Alarm_Changed"])
    log.info("Alarm summary [{}]".format(summary))
    events.postUpdate("Alarm_LastChange", summary)
