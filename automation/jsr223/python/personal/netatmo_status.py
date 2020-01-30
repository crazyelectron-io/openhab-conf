'''
----------------------------------------------------------------------------------------------------
netatmo_status.py - Handle Netatmo offline status.
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

#===================================================================================================
@rule("Netatmo Offline", description="Netatmo API watchdog timeout triggered - device offline", tags=["sensor"])
@when("Item NHC_Watchdog changed")
def netatmoStatus(event):
    if event.oldItemState is None:
        return

    netatmoStatus.log = logging.getLogger("{}.netatmoStatus".format(LOG_PREFIX))
    netatmoStatus.log.warn("Netatmo Healthy Home Coach is not responding")

    msg = "Netatmo Healthy Home Coach is not responding, please check the status of the device and online API."
    netatmoStatus.log.warning(msg)
    NotificationAction.sendBroadcastNotification(msg)

    #Echo_TTS_Livingroom.sendCommand("The " + msg)
    events.sendCommand("NHC_Watchdog", "ON")
