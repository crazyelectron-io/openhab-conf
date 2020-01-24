'''
----------------------------------------------------------------------------------------------------
hue_switch_dining.py - Hue Tap Switch dining Buttons handling rule.
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


log = logging.getLogger("{}.hue_dining".format(LOG_PREFIX))


#===================================================================================================
@rule("HueTapDining34", description="Hue dining dimmer Upper Right key - cycle scenes Dining", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 34.0")
def hue_dining_tap34(event):
    log.info("Event [{}] received".format(event.event))
    
    tap = str(event.channel).split(":")[3].split("_")[1]
    log.info("Tap detected [{}]".format(tap))
    if str(items["Light_Scene_Dining"]) == "OFF" or str(items["Light_Scene_Dining"]) == "BRIGHT":
        events.sendCommand("Light_Scene_Dining", "EVENING")
    elif str(items["Light_Scene_Dining"]) == "EVENING":
        events.sendCommand("Light_Scene_Dining", "READ")
    else:
        events.sendCommand("Light_Scene_Dining", "BRIGHT")


#===================================================================================================
@rule("HueTapDining1899", description="Hue dining tap Lower Right key - turn of dining lighting", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 18.0")
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 99.0")
def hue_dining_switch1899(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Dining", "OFF")


#===================================================================================================
@rule("HueTapDining16", description="Hue dining tap Upper Left Key - cycle scenes Livingroom", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 16.0")
def hue_dining_switch16(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Livingroom"]) == "OFF" or str(items["Light_Scene_Livingroom"]) == "READ":
        events.sendCommand("Light_Scene_Livingroom", "EVENING")
    elif str(items["Light_Scene_Livingroom"]) == "EVENING":
        events.sendCommand("Light_Scene_Livingroom", "MOVIE")
    else:
        events.sendCommand("Light_Scene_Livingroom", "READ")


#===================================================================================================
@rule("HueTapDining17", description="Hue dining tap Lower Left Key - turn off livingroom lighting", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 17.0")
def hue_dining_switch17(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Livingroom", "OFF")


#===================================================================================================
@rule("HueTapDining98", description="Hue dining tap Lower Left+Right Key - turn off livingroom and dining lighting", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 98.0")
def hue_dining_switch98(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Livingroom", "OFF")
    events.sendCommand("Light_Scene_Dining", "OFF")


#===================================================================================================
@rule("HueTapDining101", description="Hue dining tap Upper Left+Right Key - turn on livingroom and dining lighting", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_dining:tap_switch_event triggered 101.0")
def hue_dining_switch101(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Livingroom", "READ")
    events.sendCommand("Light_Scene_Dining", "READ")
