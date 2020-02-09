'''
----------------------------------------------------------------------------------------------------
hue_switch_kitchen.py - Hue Tap Switch kitchen Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200207 v02    Added Scene detection from trigger.
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when

#===================================================================================================
# @rule("HueTapkitchen34", description="Hue kitchen dimmer Upper Right key - ignored", tags=["lights"])
# @when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 34.0")
# def hueKitchenTap34(event):
#     hueKitchenTap34.log.info("Event [{}] received".format(event.event))
#     sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()

#===================================================================================================
# @rule("HueTapkitchen1899", description="Hue kitchen tap Lower Right key - ignored", tags=["lights"])
# @when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 18.0")
# @when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 99.0")
# def hueKitchenTap1899(event):
#     hueKitchenTap1899.log.info("Event [{}] received".format(event.event))
#     sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()

#===================================================================================================
@rule("HueTapkitchen16", description="Hue kitchen tap Upper Left Key - cycle scenes Kitchen", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 16.0")
def hueKitchenTap16(event):
    hueKitchenTap16.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    if items[sceneName] == StringType("OFF") or items["Light_Scene_Livingroom"] == StringType("BRIGHT"):
        events.sendCommand(sceneName, "EVENING")
    elif items[sceneName] == StringType("EVENING"):
        events.sendCommand(sceneName, "WORK")
    else:
        events.sendCommand(sceneName, "BRIGHT")

#===================================================================================================
@rule("HueTapkitchen1798", description="Hue kitchen tap Lower Left Key - turn off kitchen lighting", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 17.0")
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 98.0")
def hueKitchenTap1798(event):
    hueKitchenTap1798.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    events.sendCommand(sceneName, "OFF")

#===================================================================================================
@rule("HueTapkitchen101", description="Hue kitchen tap Upper Left+Right Key - kitchen scene WORK", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 101.0")
def hueKitchenTap101(event):
    hueKitchenTap101.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    events.sendCommand(sceneName, "WORK")
