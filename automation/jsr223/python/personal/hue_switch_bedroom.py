'''
----------------------------------------------------------------------------------------------------
hue_switch_bedroom.py - Dimmer Switch Bedroom Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
Key 1 (ON) first press:
	Turn on bedroom lighting (Scene EVENING)
Key 1 (ON) second press:
	Turn on bedroom lighting (Scene READ)
Key 1 (ON) third press:
	Turn on bedroom lighting (Scene COSY)
Key 1 (ON) fourth press:
	TUrn on bedroom lighting (Scene EVENING)
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
# from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent


log = logging.getLogger("{}.hue_bedroom".format(LOG_PREFIX))


#===================================================================================================
@rule("HueSwBed1000", description="Hue bedroom dimmer Key 1 (ON) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 1000.0")
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 1000.0")
def hue_bedroom_switch1000(event):
    log.info("Event [{}] received".format(event.event))
    
    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed1001", description="Hue bedroom dimmer Key 1 (ON) Hold - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 1001.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 1001.0")
def hue_bedroom_switch1001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if items.Light_Dim_BedroomLeft == 0 or items.Light_Dim_BedroomLeft == items.Bedroom_Brightness_READ:
        log.info("Turn on left bedroom light to EVENING scene")
        events.sendCommand("Light_Dim_BedroomLeft", str(items["Bedroom_Brightness_EVENING"]))
        events.sendCommand("Light_ColorTemp_BedroomLeft", str(items["Bedroom_ColorTemp_EVENING"]))
    elif items.Light_Dim_BedroomLeft == items.Bedroom_Brightness_EVENING:
        log.info("Turn on left bedroom light to READ scene")
        events.sendCommand("Light_Dim_BedroomLeft", str(items["Bedroom_Brightness_READ"]))
        events.sendCommand("Light_ColorTemp_BedroomLeft", str(items["Bedroom_ColorTemp_READ"]))
    elif items.Light_Dim_BedroomLeft == items.Bedroom_Brightness_READ:
        log.info("Turn left bedroom light back to EVENING scene")
        events.sendCommand("Light_Dim_BedroomLeft", str(items["Bedroom_Brightness_EVENING"]))
        events.sendCommand("Light_ColorTemp_BedroomLeft", str(items["Bedroom_ColorTemp_EVENING"]))


#===================================================================================================
@rule("HueSwBed1002", description="Hue bedroom dimmer Key 1 (ON) Short release - turn off hall/kitchen light", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 1002.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 1002.0")
def hue_bedroom_switch1002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items.Light_Scene_Bedroom) == "OFF":
        log.info("First Button 1 (ON) Short Release - Set bedroom Scene to EVENING")
        events.sendCommand("Light_Scene_Bedroom", "EVENING")
    elif str(items.Light_Scene_Bedroom) == "EVENING":
        log.info("Second Button 1 (ON) Short Release - Set bedroom Scene to READ")
        events.sendCommand("Light_Scene_Bedroom", "READ")
    elif str(items.Light_Scene_Bedroom) == "READ":
        log.info("Third Button 1 (ON) Short Release - Set bedroom Scene to COSY")
        events.sendCommand("Light_Scene_Bedroom", "COSY")
    else:
        log.info("Fourth Button 1 (ON) Short Release state - reset to EVENING scene")
        events.sendCommand("Light_Scene_Bedroom", "EVENING")


#===================================================================================================
@rule("HueSwBed1003", description="Hue bedroom dimmer Key 1 (ON) Long release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 1003.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 1003.0")
def hue_bedroom_switch1003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed2000", description="Hue bedroom dimmer Key 2 (INCREASE) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 2000.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 2000.0")
def hue_bedroom_switch2000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed20012", description="Hue bedroom dimmer Key 2 (INCREASE) - increase brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 2002.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 2002.0")
def hue_bedroom_switch20012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if items.Light_Dim_BedroomLeft != 0:
        events.sendCommand("Light_Dim_BedroomLeft", "INCREASE")
    if items.Light_Dim_BedroomRight != 0:
        events.sendCommand("Light_Dim_BedroomRight", "INCREASE")


#===================================================================================================
@rule("HueSwBed2003", description="Hue bedroom dimmer Key 2 (INCREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 2003.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 2003.0")
def hue_bedroom_switch2003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed3000", description="Hue bedroom dimmer Key 3 (DECREASE) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 3000.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 3000.0")
def hue_bedroom_switch3000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed30012", description="Hue bedroom dimmer Key 3 (DECREASE) - decrease brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 3002.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 3002.0")
def hue_bedroom_switch30012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if items.Light_Dim_BedroomLeft != 0:
        events.sendCommand("Light_Dim_BedroomLeft", "DECREASE")
    if items.Light_Dim_BedroomRight != 0:
        events.sendCommand("Light_Dim_BedroomRight", "DECREASE")


#===================================================================================================
@rule("HueSwBed3003", description="Hue bedroom dimmer Key 3 (DECREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 3003.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 3003.0")
def hue_bedroom_switch3003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed4000", description="Hue bedroom dimmer Key 4 (OFF) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 4000.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 4000.0")
def hue_bedroom_switch4000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBed4001", description="Hue bedroom dimmer Key 4 (OFF) Hold - Turn of bedroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 4001.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 4001.0")
def hue_bedroom_switch4001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Bedroom", "OFF")


#===================================================================================================
@rule("HueSwBed4002", description="Hue bedroom dimmer Key 4 (OFF) Short Release - Turn of bedroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 4002.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 4002.0")
def hue_bedroom_switch4002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items.Light_Scene_Bedroom) != "OFF":
        events.sendCommand("Light_Scene_Bedroom", "OFF")


#===================================================================================================
@rule("HueSwBed4003", description="Hue bedroom dimmer Key 4 (OFF) Long Release - Turn of all bedroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_rbed:dimmer_switch_event triggered 4003.0")
@when("Channel hue:0820:0017882ec5b3:dim_lbed:dimmer_switch_event triggered 4003.0")
def hue_bedroom_switch4003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Bedroom", "OFF")
    events.sendCommand("Light_Scene_Livingroom", "OFF")
    events.sendCommand("Light_Scene_Dining", "OFF")
    events.sendCommand("Alarm_Status", "ARMED_HOME")
