'''
----------------------------------------------------------------------------------------------------
hue_switch_toilet.py - Dimmer Switch toilet Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when

#===================================================================================================
# @rule("HueSwToilet1000", description="Hue toilet dimmer Key 1 (ON) Initial Press - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1000.0")
# def hue_toilet_switch1000(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
# @rule("HueSwToilet1001", description="Hue toilet dimmer Key 1 (ON) Hold - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1001.0")
# def hue_toilet_switch1001(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("HueSwToilet1002", description="Hue toilet dimmer Key 1 (ON) Short release - turn off hall/kitchen light", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1002.0")
def hueToiletSwitch1002(event):
    hueToiletSwitch1002.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3]
    # log.info("Switch detected [{}]".format(switch))
    if items["Light_Scene_Toilet"] == StringType("OFF"):
        events.sendCommand("Light_Scene_Toilet", "EVENING")
    elif items["Light_Scene_Toilet"] == StringType("EVENING"):
        events.sendCommand("Light_Scene_Toilet", "READ")
    elif items["Light_Scene_Toilet"] == StringType("READ"):
        events.sendCommand("Light_Scene_Toilet", "BRIGHT")
    else:
        events.sendCommand("Light_Scene_Toilet", "EVENING")

#===================================================================================================
# @rule("HueSwToilet1003", description="Hue toilet dimmer Key 1 (ON) Long release - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1003.0")
# def hue_toilet_switch1003(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
# @rule("HueSwToilet2000", description="Hue toilet dimmer Key 2 (INCREASE) Initial Press - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2000.0")
# def hue_toilet_switch2000(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("HueSwToilet20012", description="Hue toilet dimmer Key 2 (INCREASE) - increase brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2002.0")
def hueToiletSwitch20012(event):
    hueToiletSwitch20012.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3]
    if items["Light_Scene_Toilet"] != StringType("OFF"):
        events.sendCommand("gLight_Brightness_toilet", "INCREASE")

#===================================================================================================
# @rule("HueSwToilet2003", description="Hue toilet dimmer Key 2 (INCREASE) Long Release - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2003.0")
# def hue_toilet_switch2003(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
# @rule("HueSwToilet3000", description="Hue toilet dimmer Key 3 (DECREASE) Initial Pressed - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3000.0")
# def hue_toilet_switch3000(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("HueSwToilet30012", description="Hue toilet dimmer Key 3 (DECREASE) - decrease brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3002.0")
def hueToiletSwitch30012(event):
    hueToiletSwitch30012.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3]
    if items["Light_Scene_Toilet"] != StringType("OFF"):
        events.sendCommand("gLight_Brightness_toilet", "DECREASE")

#===================================================================================================
# @rule("HueSwToilet3003", description="Hue toilet dimmer Key 3 (DECREASE) Long Release - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3003.0")
# def hue_toilet_switch3003(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
# @rule("HueSwToilet4000", description="Hue toilet dimmer Key 4 (OFF) Initial Pressed - ignored", tags=["lights"])
# @when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4000.0")
# def hue_toilet_switch4000(event):
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("HueSwToilet4001", description="Hue toilet dimmer Key 4 (OFF) Hold - Turn of toilet lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4001.0")
def hueToiletSwitch4001(event):
    hueToiletSwitch4001.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3]
    events.sendCommand("Light_Scene_Toilet", "OFF")

#===================================================================================================
@rule("HueSwToilet4002", description="Hue toilet dimmer Key 4 (OFF) Short Release - Turn of toilet lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4002.0")
def hueToiletSwitch4002(event):
    hueToiletSwitch4002.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3].split("_")[1]
    # log.info("Switch detected [{}]".format(switch))
    if items["Light_Scene_Toilet"] != OFF:
        events.sendCommand("Light_Scene_Toilet", "OFF")

#===================================================================================================
@rule("HueSwToilet4003", description="Hue toilet dimmer Key 4 (OFF) Long Release - Turn of all toilet lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4003.0")
def hueToiletSwitch4003(event):
    hueToiletSwitch4003.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3]
    events.sendCommand("Light_Scene_Toilet", "OFF")