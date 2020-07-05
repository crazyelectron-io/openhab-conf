'''
----------------------------------------------------------------------------------------------------
hue_tap_bathroom.py - Hue Tap Switch bathroom Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200613 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when

#===================================================================================================
# Select Bathroom Shower light scene
@rule("Hue Tap Bathroom 34", description="Hue Tap Upper Right Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 34.0")
def hueBathroomTap34(event):
    hueBathroomTap34.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize() + "Shower"
    hueBathroomTap34.log.info("Scene Name [{}]".format(sceneName))
    if items[sceneName] == StringType("OFF") or items[sceneName] == StringType("BRIGHT"):
        events.sendCommand(sceneName, "EVENING")
    elif items[sceneName] == StringType("EVENING"):
        events.sendCommand(sceneName, "READ")
    else:
        events.sendCommand(sceneName, "BRIGHT")

#===================================================================================================
@rule("Hue Tap Bathroom 18", description="Hue Tap Lower Right Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 18.0")
def hueBathroomTap18(event):
    hueBathroomTap18.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize() + "Shower"
    hueBathroomTap34.log.info("Scene Name [{}]".format(sceneName))
    events.sendCommand(sceneName, "OFF")

#===================================================================================================
@rule("Hue Tap Bathroom 99", description="Hue Tap Lower Right Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 99.0")
def hueBathroomTap99(event):
    hueBathroomTap99.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize() + "Shower"
    events.sendCommand(sceneName, "OFF")

#===================================================================================================
# Select Bathroom Sink light scene
@rule("Hue Tap Bathroom 16", description="Hue Tap Upper Left Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 16.0")
def hueBathroomTap16(event):
    hueBathroomTap16.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize() + "Sink"
    if items[sceneName] == StringType("OFF") or items[sceneName] == StringType("BRIGHT"):
        events.sendCommand(sceneName, "EVENING")
    elif items[sceneName] == StringType("EVENING"):
        events.sendCommand(sceneName, "READ")
    else:
        events.sendCommand(sceneName, "BRIGHT")

#===================================================================================================
@rule("Hue Tap Bathroom 17", description="Hue dining tap Lower Left Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 17.0")
def hueBathroomTap17(event):
    hueBathroomTap17.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize() + "Sink"
    events.sendCommand(sceneName, "OFF")

#===================================================================================================
@rule("Hue Tap Bathroom 98", description="Hue Tap Lower Left+Right Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 98.0")
def hueBathroomTap98(event):
    hueBathroomTap98.log.info("Event [{}] received".format(event.event))
    sceneNamePart = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    events.sendCommand(sceneNamePart + "Sink", "OFF")
    events.sendCommand(sceneNamePart + "Shower", "OFF")

#===================================================================================================
# Select Bathroom light scene
@rule("Hue Tap Bath101", description="Hue Tap Upper Left+Right Key pressed", tags=["lights"])
@when("Channel hue:0830:001788FFFE6D2293:tap_bathroom:tap_switch_event triggered 101.0")
def hueBathroomTap101(event):
    hueBathroomTap101.log.info("Event [{}] received".format(event.event))
    sceneNamePart = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    if items[sceneNamePart + "Sink"] == StringType("OFF") or items[sceneNamePart + "Sink"] == StringType("BRIGHT"):
        events.sendCommand(sceneNamePart + "Sink", "EVENING")
        events.sendCommand(sceneNamePart + "Shower", "EVENING")
    elif items[sceneNamePart + "Sink"] == StringType("EVENING"):
        events.sendCommand(sceneNamePart + "Sink", "READ")
        events.sendCommand(sceneNamePart + "Shower", "READ")
    else:
        events.sendCommand(sceneNamePart + "Sink", "BRIGHT")
        events.sendCommand(sceneNamePart + "Shower", "BRIGHT")
