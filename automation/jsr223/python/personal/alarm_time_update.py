'''
----------------------------------------------------------------------------------------------------
alarm_time_update.py - Handle alarm change commands and trigger other actions.
----------------------------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
# from core.log import logging
import configuration
reload(configuration)
# from configuration import LOG_PREFIX

#===================================================================================================
@rule("Alarm Time Update", description="The alarm status has changed, retrieve user and time of day summary", tags=["alarm"])
@when("Item Alarm_Time changed")
def alarmTimeUpdate(event):
    if event.oldItemState is None:
        return
    summary = str(items["Alarm_User"]) .split(' ')[0] + " at " + ((str(items["Alarm_Time"]) .split('T')[1]).split('\\.')[0])[0:5] + " via " + str(items["Alarm_Changed"]) 
    alarmTimeUpdate.log.info("Alarm summary [{}]".format(summary))
    events.postUpdate("Alarm_LastChange", summary)