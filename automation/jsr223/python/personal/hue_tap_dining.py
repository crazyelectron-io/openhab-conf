'''
----------------------------------------------------------------------------------------------------
hue_switch_dining.py - Hue Tap Switch dining Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200204 v02    Retrieve light area from trigger channel.
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when

#===================================================================================================
@rule("Hue Tap Dining 34", description="Hue Tap Upper Right Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 34.0")
def hueDiningTap34(event):
    hueDiningTap34.log.info("Event [{}] received".format(event.event))
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    hueDiningTap34.log.info("Scene Name [{}]".format(sceneName))
    if items[sceneName] == StringType("OFF") or items["Light_Scene_Livingroom"] == StringType("BRIGHT"):
        events.sendCommand(sceneName, "EVENING")
    elif items["Light_Scene_Livingroom"] == StringType("EVENING"):
        events.sendCommand(sceneName, "READ")
    else:
        events.sendCommand(sceneName, "BRIGHT")

#===================================================================================================
@rule("Hue Tap Dining 18", description="Hue Tap Lower Right Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 18.0")
def hueDiningTap18(event):
    hueDiningTap18.log.info("Event [{}] received".format(event.event))
    # tap = str(event.channel).split(":")[3].split("_")[1]
    sceneName = "Light_Scene_" + (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    events.sendCommand(sceneName, "OFF")

#===================================================================================================
@rule("Hue Tap Dining 99", description="Hue Tap Lower Right Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 99.0")
def hueDiningTap99(event):
    hueDiningTap99.log.info("Event [{}] received".format(event.event))
    # tap = str(event.channel).split(":")[3].split("_")[1]
    events.sendCommand("Light_Scene_Dining", "OFF")

#===================================================================================================
@rule("Hue Tap Dining 16", description="Hue Tap Upper Left Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 16.0")
def hueDiningTap16(event):
    hueDiningTap16.log.info("Event [{}] received".format(event.event))
    # tap = str(event.channel).split(":")[3]
    if items["Light_Scene_Livingroom"] == StringType("OFF") or items["Light_Scene_Livingroom"] == StringType("READ"):
        events.sendCommand("Light_Scene_Livingroom", "EVENING")
    elif items["Light_Scene_Livingroom"] == StringType("EVENING"):
        events.sendCommand("Light_Scene_Livingroom", "MOVIE")
    else:
        events.sendCommand("Light_Scene_Livingroom", "READ")

#===================================================================================================
@rule("Hue Tap Dining 17", description="Hue dining tap Lower Left Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 17.0")
def hueDiningTap17(event):
    hueDiningTap17.log.info("Event [{}] received".format(event.event))
    # tap = str(event.channel).split(":")[3].split("_")[1]
    events.sendCommand("Light_Scene_Livingroom", "OFF")

#===================================================================================================
@rule("Hue Tap Dining 98", description="Hue Tap Lower Left+Right Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 98.0")
def hueDiningTap98(event):
    hueDiningTap98.log.info("Event [{}] received".format(event.event))
    # tap = str(event.channel).split(":")[3].split("_")[1]
    events.sendCommand("Light_Scene_Livingroom", "OFF")
    events.sendCommand("Light_Scene_Dining", "OFF")

#===================================================================================================
@rule("Hue Tap Dining 101", description="Hue Tap Upper Left+Right Key pressed", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 101.0")
def hueDiningTap101(event):
    hueDiningTap101.log.info("Event [{}] received".format(event.event))
    # tap = str(event.channel).split(":")[3].split("_")[1]
    events.sendCommand("Light_Scene_Livingroom", "READ")
    events.sendCommand("Light_Scene_Dining", "READ")