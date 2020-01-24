'''
----------------------------------------------------------------------------------------------------
hue_switch_kitchen.py - Hue Tap Switch kitchen Buttons handling rule.
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


log = logging.getLogger("{}.hue_kitchen".format(LOG_PREFIX))


#===================================================================================================
@rule("HueTapkitchen34", description="Hue kitchen dimmer Upper Right key - ignored", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 34.0")
def hue_kitchen_tap34(event):
    log.info("Event [{}] received".format(event.event))
    
    tap = str(event.channel).split(":")[3].split("_")[1]
    log.info("Tap detected [{}]".format(tap))


#===================================================================================================
@rule("HueTapkitchen1899", description="Hue kitchen tap Lower Right key - ignored", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 18.0")
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 99.0")
def hue_kitchen_switch1899(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueTapkitchen16", description="Hue kitchen tap Upper Left Key - cycle scenes Kitchen", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 16.0")
def hue_kitchen_switch16(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Kitchen"]) == "OFF" or str(items["Light_Scene_Kitchen"]) == "BRIGHT":
        events.sendCommand("Light_Scene_Kitchen", "EVENING")
    elif str(items["Light_Scene_Kitchen"]) == "EVENING":
        events.sendCommand("Light_Scene_Kitchen", "WORK")
    else:
        events.sendCommand("Light_Scene_Kitchen", "BRIGHT")


#===================================================================================================
@rule("HueTapkitchen1798", description="Hue kitchen tap Lower Left Key - turn off kitchen lighting", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 17.0")
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 98.0")
def hue_kitchen_switch1798(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Kitchen", "OFF")


#===================================================================================================
@rule("HueTapkitchen101", description="Hue kitchen tap Upper Left+Right Key - kitchen scene WORK", tags=["lights"])
@when("Channel hue:0830:0017882ec5b3:tap_kitchen:tap_switch_event triggered 101.0")
def hue_kitchen_switch101(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Kitchen", "WORK")
