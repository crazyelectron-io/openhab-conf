'''
----------------------------------------------------------------------------------------------------
xmas_lights.py - Handle Christmas lighting.
----------------------------------------------------------------------------------------------------
Changelog:
20201223 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
import configuration
reload(configuration)
from core.actions import NotificationAction

# #===================================================================================================
# @rule("Xmas Scene Switch", description="Turn Xmas lights on and off based on the Day Mode", tags=["xmas"])
# @when("Item Day_Mode changed")
# def xmasSceneSwitch(event):
#     if isinstance(event.oldItemState, UnDefType) or event.oldItemState is None:
#         return
#     xmasSceneSwitch.log.info("{name} changed to {newState} from {oldState}".format(name=event.itemName, newState=event.itemState, oldState=event.oldItemState))
#     # Determine the Scene to select
#     command = "OFF" if str(ir.getItem("Day_Mode").state) == "DAY" else "ON"
#     xmasSceneSwitch.log.info("Send command [{}] to Xmas lights".format(command))
#     events.sendCommand("Shelly_Xmas_Switch", command)
#     msg = "Day mode change: Xmas lights switched to Scene " + command
#     NotificationAction.sendBroadcastNotification(msg)


#===================================================================================================
@rule("Winter Livingroom Switch", description="Turn Winter lights in the livingroom on and off", tags=["xmas"])
@when("Item Light_Scene_Livingroom changed")
def winterLivingRoomSwitch(event):
    if isinstance(event.oldItemState, UnDefType) or event.oldItemState is None:
        return
    winterLivingRoomSwitch.log.info("{name} changed to {newState} from {oldState}".format(name=event.itemName, newState=event.itemState, oldState=event.oldItemState))
    # Determine the Scene to select
    command = "OFF" if str(ir.getItem("Light_Scene_Livingroom").state) == "OFF" else "ON"
    winterLivingRoomSwitch.log.info("Send command [{}] to Winter livingroom lights".format(command))
    events.sendCommand("Shelly_SideTable_Switch", command)
    msg = "Livingroom lights change: Winter lights switched to Scene " + command
    NotificationAction.sendBroadcastNotification(msg)
