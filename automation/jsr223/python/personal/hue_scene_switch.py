'''
----------------------------------------------------------------------------------------------------
hue_scene_switch.py - Switch lights on at sunset and off at sunrise (depending on cloudiness).
----------------------------------------------------------------------------------------------------
Changelog:
20200121 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
from core.actions import NotificationAction

log = logging.getLogger("{}.hue_scene_switch".format(LOG_PREFIX))


#==================================================================================================
@rule("HueDayNight", description="Turn lights on and off based on the Day Mode", tags=["astro"])
@when("Item Day_Mode changed")
def hue_scene_switch(event):
    log.info("{name} changed to {newState} from {oldState}".format(name=event.itemName, newState=event.itemState, oldState=event.oldItemState))
    if event.oldItemState == NULL:
        return

    # Determine the Scene to select (if any)
    command = "OFF" if items["Day_Mode"] == "DAY" else "EVENING" if items["Day_Mode"] == "EVENING" else ""
	
    if command != "":
        log.info("Send command {cmd} to Light Scenes".format(cmd=command))
		# gLight_Automatic.sendCommand(command)
        events.sendCommand("Light_Scene_Livingroom")
        events.sendCommand("Light_Scene_Dining")
        events.sendCommand("Light_Scene_Kitchen")
        events.sendCommand("Light_Scene_Hall")
        events.sendCommand("Light_Scene_Outside")
		# Light_Scene_Lodge.sendCommand(command)
        msg = "Day mode change: lights switched to Scene " + command
        NotificationAction.sendBroadcastNotification(msg)
