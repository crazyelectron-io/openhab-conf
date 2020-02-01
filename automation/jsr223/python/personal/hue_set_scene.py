
'''
----------------------------------------------------------------------------------------------------
hue_set_scene.py - Change lighting in area to the specified scene.
----------------------------------------------------------------------------------------------------
Changelog:
20200201 v02    Fixed ColorTemp group sendCommand.
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX

#==================================================================================================
@rule("Set Hue Scene", description="Change lighting in area to the specified scene", tags=["lights"])
@when("Item Light_Scene_Livingroom changed")
@when("Item Light_Scene_Kitchen changed")
@when("Item Light_Scene_Dining changed")
@when("Item Light_Scene_Hall changed")
@when("Item Light_Scene_HallCeiling changed")
@when("Item Light_Scene_Bathroom changed")
@when("Item Light_Scene_Bedroom changed")
@when("Item Light_Scene_Lodge changed")
@when("Item Light_Scene_Guestroom changed")
@when("Item Light_Scene_Laundry changed")
@when("Item Light_Scene_Outside changed")
def hueSetScene(event):
    hueSetScene.log = logging.getLogger("{}.hueSetScene".format(LOG_PREFIX))
    hueSetScene.log.info("[{}] changed, state is [{}], previous state [{}]".format(event.itemName, event.itemState, event.oldItemState))
    if event.oldItemState is None:
        return

    lightArea = event.itemName.split('_')[2]
    scene = str(event.itemState)
    # hueSetScene.log.debug("Received update [{}] for area [{}]".format(scene, lightArea))
    lightGroup = ir.getItem("gLight_Brightness_" + lightArea)
    # hueSetScene.log.debug("Set Lighting Scene to [{}] for [{}]".format(scene, str(lightGroup.name)))

    if scene == "OFF":
        events.sendCommand(str(lightGroup.name), "OFF")
    elif scene == "EVENING" or scene == "READ" or scene == "WORK" or scene == "BRIGHT" or scene == "MOVIE":
        brightnessGroup = ir.getItem("gLight_Brightness_" + lightArea)
        brightness = ir.getItem(lightArea + "_Brightness_" + event.itemState.toString()).state.toString()
        hueSetScene.log.info("Brightness command [{}], group [{}]".format(brightness, brightnessGroup.name))
        events.sendCommand(str(brightnessGroup.name), brightness)
        if str(lightArea) != "Lodge" and str(lightArea) != "Outside":
            colorTempGroup = ir.getItem("gLight_ColorTemp_" + lightArea)
            colorTemp = ir.getItem(lightArea + "_ColorTemp_" + event.itemState.toString()).state.toString()
            hueSetScene.log.info("ColorTemp command [{}], group [{}]".format(colorTemp, colorTempGroup.name))
            events.sendCommand(str(colorTempGroup.name), colorTemp)
    else:
        hueSetScene.log.warn("Unknown Scene command [{}] received, restore previous state [{}]".format(scene, event.oldItemState))
        events.postUpdate(str(event.itemName), str(event.oldItemState))
