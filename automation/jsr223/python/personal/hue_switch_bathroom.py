'''
----------------------------------------------------------------------------------------------------
hue_switch_event.py - Dimmer Switch Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
# from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent

log = logging.getLogger("{}.hue_switch".format(LOG_PREFIX))

#===================================================================================================
@rule("Hue Switch Event 1000", description="Hue dimmer Key 1 (ON) Initial Pressed", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1000.0")
def hueSwitchEvent1000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 1001", description="Hue dimmer Key 1 (ON) Hold", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1001.0")
def hueSwitchEvent1001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 1002", description="Hue dimmer Key 1 (ON) Short Released", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1002.0")
def hueSwitchEvent1002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]

    if str(ir.getItem("Light_Scene_Bathroom").state) == "OFF":
        log.info("First Button 1 (ON) Short Release - Set Bathroom Scene to EVENING")
        events.sendCommand("Light_Scene_Bathroom", "EVENING")
    elif str(ir.getItem("Light_Scene_Bathroom").state) == "EVENING":
        log.info("Second Button 1 (ON) Short Release - Set Bathroom Scene to READ")
        events.sendCommand("Light_Scene_Bathroom", "READ")
    elif str(ir.getItem("Light_Scene_Bathroom").state) == "READ":
        log.info("Third Button 1 (ON) Short Release - Set Bathroom Scene to BRIGHT")
        events.sendCommand("Light_Scene_Bathroom", "BRIGHT")
    else:
        log.info("Fourth Button 1 (ON) Short Release state - reset to EVENING scene")
        events.sendCommand("Light_Scene_Bathroom", "EVENING")


#===================================================================================================
@rule("Hue Switch Event 1003", description="Hue dimmer Key 1 (ON) Long release", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1003.0")
def hueSwitchEvent1003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 2000", description="Hue dimmer Key 2 (INCREASE) Initial Pressed", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2000.0")
def hueSwitchEvent2000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 20012", description="Hue dimmer Key 2 (INCREASE) Hold", tags=["lights","switch","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2002.0")
def hueSwitchEvent20012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]

    if ir.getItem("Light_Scene_Bathroom != OFF").state:
        events.sendCommand("gLight_Brightness_Bathroom", "INCREASE")


#===================================================================================================
@rule("Hue Switch Event 2003", description="Hue dimmer Key 2 (INCREASE) Long Release", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2003.0")
def hueSwitchEvent2003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 3000", description="Hue dimmer Key 3 (DECREASE) Initial Pressed - ignored", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3000.0")
def hueSwitchEvent3000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 30012", description="Hue dimmer Key 3 (DECREASE) - decrease brightness", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3002.0")
def hueSwitchEvent30012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]

    if ir.getItem("Light_Scene_Bathroom != OFF").state:
        events.sendCommand("gLight_Brightness_Bathroom", "DECREASE")


#===================================================================================================
@rule("Hue Switch Event 3003", description="Hue dimmer Key 3 (DECREASE) Long Release - ignored", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3003.0")
def hueSwitchEvent3003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 4000", description="Hue dimmer Key 4 (OFF) Initial Pressed", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4000.0")
def hueSwitchEvent4000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]


#===================================================================================================
@rule("Hue Switch Event 4001", description="Hue dimmer Key 4 (OFF) Hold", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4001.0")
def hueSwitchEvent4001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]

    events.sendCommand("Light_Scene_Bathroom", "OFF")


#===================================================================================================
@rule("Hue Switch Event 4002", description="Hue dimmer Key 4 (OFF) Short Release", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4002.0")
def hueSwitchEvent4002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]

    if str(ir.getItem("Light_Scene_Bathroom").state) != "OFF":
        events.sendCommand("Light_Scene_Bathroom", "OFF")


#===================================================================================================
@rule("Hue Switch Event 4003", description="Hue Bathroom dimmer Key 4 (OFF) Long Release", tags=["lights","switch"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4003.0")
def hueSwitchEvent4003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]

    events.sendCommand("Light_Scene_Bathroom", "OFF")
