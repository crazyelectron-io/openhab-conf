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
from core.actions import NotificationAction

#==================================================================================================
@rule("Hue Scene Switch", description="Turn lights on and off based on the Day Mode", tags=["astro"])
@when("Item Day_Mode changed")
def hueSceneSwitch(event):
    if event.oldItemState is None:
        return
    hueSceneSwitch.log.info("{name} changed to {newState} from {oldState}".format(name=event.itemName, newState=event.itemState, oldState=event.oldItemState))
    # Determine the Scene to select (if any)
    command = "OFF" if str(ir.getItem("Day_Mode").state) == "DAY" else "EVENING" if str(ir.getItem("Day_Mode").state) == "EVENING" else ""
    if command != "":
        hueSceneSwitch.log.info("Send command [{}] to Light Scenes".format(command))
		# gLight_Automatic.sendCommand(command)
        events.sendCommand("Light_Scene_Livingroom", command)
        events.sendCommand("Light_Scene_Dining", command)
        events.sendCommand("Light_Scene_Kitchen", command)
        events.sendCommand("Light_Scene_Hall", command)
        events.sendCommand("Light_Scene_Outside", command)
		# Light_Scene_Lodge.sendCommand(command)
        if command == "OFF":
            events.sendCommand("Light_Scene_HallCeiling", command)
        msg = "Day mode change: lights switched to Scene " + command
        NotificationAction.sendBroadcastNotification(msg)