'''
----------------------------------------------------------------------------------------------------
hue_switch_event.py - Dimmer Switch Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200205 v02    Retrieve light area from trigger channel.
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
# from core.log import logging, LOG_PREFIX
# import configuration
# reload(configuration)
# from configuration import LOG_PREFIX

# #===================================================================================================
# @rule("Hue Switch Event1000", description="Hue Dimmer Switch Key 1 (ON) Initial Pressed", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1000.0")
# def hueSwitchEvent1000(event):
#     hueSwitchEvent1000.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

# #===================================================================================================
# @rule("Hue Switch Event1001", description="Hue Dimmer Switch Key 1 (ON) Hold", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1001.0")
# def hueSwitchEvent1001(event):
#     hueSwitchEvent1001.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("Hue Switch Event1002", description="Hue Dimmer Switch Key 1 (ON) Short Released", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1002.0")
def hueSwitchEvent1002(event):
    hueSwitchEvent1002.log.info("Event [{}] received".format(event.event))
    # switch = (str(event.channel).split(":")[3].split("_")[1]).capitalize()
    if items["Light_Scene_Bathroom"] == StringType("OFF"):
        # hueSwitchEvent1002.log.info("First Button 1 (ON) Short Release - Set Bathroom Scene to EVENING")
        events.sendCommand("Light_Scene_Bathroom", "EVENING")
    elif items["Light_Scene_Bathroom"] == StringType("EVENING"):
        # hueSwitchEvent1002.log.info("Second Button 1 (ON) Short Release - Set Bathroom Scene to READ")
        events.sendCommand("Light_Scene_Bathroom", "READ")
    elif items["Light_Scene_Bathroom"] == StringType("READ"):
        # hueSwitchEvent1002.log.info("Third Button 1 (ON) Short Release - Set Bathroom Scene to BRIGHT")
        events.sendCommand("Light_Scene_Bathroom", "BRIGHT")
    else:
        # hueSwitchEvent1002.log.info("Fourth Button 1 (ON) Short Release state - reset to EVENING scene")
        events.sendCommand("Light_Scene_Bathroom", "EVENING")

# #===================================================================================================
# @rule("Hue Switch Event1003", description="Hue Dimmer Switch Key 1 (ON) Long Released", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1003.0")
# def hueSwitchEvent1003(event):
#     hueSwitchEvent1003.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]


# #===================================================================================================
# @rule("Hue Switch Event2000", description="Hue Dimmer Switch Key 2 (INCREASE) Initial Pressed", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2000.0")
# def hueSwitchEvent2000(event):
#     hueSwitchEvent2000.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("Hue Switch Event2001.2002", description="Hue Dimmer Switch Key 2 (INCREASE) Hold", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2002.0")
def hueSwitchEvent20012(event):
    hueSwitchEvent20012.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3].split("_")[1]
    if items["Light_Scene_Bathroom"] != StringType("OFF"):
        events.sendCommand("gLight_Brightness_Bathroom", "INCREASE")

# #===================================================================================================
# @rule("Hue Switch Event2003", description="Hue Dimmer Switch Key 2 (INCREASE) Long Released", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2003.0")
# def hueSwitchEvent2003(event):
#     hueSwitchEvent2003.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

# #===================================================================================================
# @rule("Hue Switch Event 3000", description="Hue Dimmer Switch Key 3 (DECREASE) Initial Pressed", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3000.0")
# def hueSwitchEvent3000(event):
#     hueSwitchEvent3000.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("Hue Switch Event3001.3002", description="Hue dimmer Key 3 (DECREASE)", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3002.0")
def hueSwitchEvent30012(event):
    hueSwitchEvent30012.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3].split("_")[1]
    if items["Light_Scene_Bathroom"] != StringType("OFF"):
        events.sendCommand("gLight_Brightness_Bathroom", "DECREASE")

# #===================================================================================================
# @rule("Hue Switch Event3003", description="Hue Dimmer Switch Key 3 (DECREASE) Long Released", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3003.0")
# def hueSwitchEvent3003(event):
#     hueSwitchEvent3003.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

# #===================================================================================================
# @rule("Hue Switch Event4000", description="Hue Dimmer Switch Key 4 (OFF) Initial Pressed", tags=["lights","switch"])
# @when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4000.0")
# def hueSwitchEvent4000(event):
#     hueSwitchEvent4000.log.info("Event [{}] received".format(event.event))
#     switch = str(event.channel).split(":")[3].split("_")[1]

#===================================================================================================
@rule("Hue Switch Event4001", description="Hue Dimmer Switch Key 4 (OFF) Hold", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4001.0")
def hueSwitchEvent4001(event):
    hueSwitchEvent4001.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3].split("_")[1]
    events.sendCommand("Light_Scene_Bathroom", "OFF")

#===================================================================================================
@rule("Hue Switch Event4002", description="Hue Dimmer SwitchKey 4 (OFF) Short Released", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4002.0")
def hueSwitchEvent4002(event):
    hueSwitchEvent4002.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3].split("_")[1]
    if items["Light_Scene_Bathroom"] != StringType("OFF"):
        events.sendCommand("Light_Scene_Bathroom", "OFF")

#===================================================================================================
@rule("Hue Switch Event4003", description="Hue Dimmer Switch Key 4 (OFF) Long Released", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4003.0")
def hueSwitchEvent4003(event):
    hueSwitchEvent4003.log.info("Event [{}] received".format(event.event))
    # switch = str(event.channel).split(":")[3]
    events.sendCommand("Light_Scene_Bathroom", "OFF")
