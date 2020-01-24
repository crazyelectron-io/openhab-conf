'''
----------------------------------------------------------------------------------------------------
hue_switch_bathroom.py - Dimmer Switch Bathroom Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
Key 1 (ON) first press:
	Turn on Bathroom lighting (Scene EVENING)
Key 1 (ON) second press:
	Turn on Bathroom lighting (Scene READ)
Key 1 (ON) third press:
	Turn on Bathroom lighting (Scene BRIGHT)
Key 1 (ON) fourth press:
	TUrn on Bathroom lighting (Scene EVENING)
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
# from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent


log = logging.getLogger("{}.hue_bathroom".format(LOG_PREFIX))


#===================================================================================================
@rule("HueSwBath1000", description="Hue Bathroom dimmer Key 1 (ON) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1000.0")
def hue_bathroom_switch1000(event):
    log.info("Event [{}] received".format(event.event))
    
    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath1001", description="Hue Bathroom dimmer Key 1 (ON) Hold - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1001.0")
def hue_bathroom_switch1001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath1002", description="Hue Bathroom dimmer Key 1 (ON) Short release - turn off hall/kitchen light", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1002.0")
def hue_bathroom_switch1002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Bathroom"]) == "OFF":
        log.info("First Button 1 (ON) Short Release - Set Bathroom Scene to EVENING")
        events.sendCommand("Light_Scene_Bathroom", "EVENING")
    elif str(items["Light_Scene_Bathroom"]) == "EVENING":
        log.info("Second Button 1 (ON) Short Release - Set Bathroom Scene to READ")
        events.sendCommand("Light_Scene_Bathroom", "READ")
    elif str(items["Light_Scene_Bathroom"]) == "READ":
        log.info("Third Button 1 (ON) Short Release - Set Bathroom Scene to BRIGHT")
        events.sendCommand("Light_Scene_Bathroom", "BRIGHT")
    else:
        log.info("Fourth Button 1 (ON) Short Release state - reset to EVENING scene")
        events.sendCommand("Light_Scene_Bathroom", "EVENING")


#===================================================================================================
@rule("HueSwBath1003", description="Hue Bathroom dimmer Key 1 (ON) Long release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 1003.0")
def hue_bathroom_switch1003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath2000", description="Hue Bathroom dimmer Key 2 (INCREASE) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2000.0")
def hue_bathroom_switch2000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath20012", description="Hue Bathroom dimmer Key 2 (INCREASE) - increase brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2002.0")
def hue_bathroom_switch20012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Bathroom"]) != "OFF":
        events.sendCommand("gLight_Brightness_Bathroom", "INCREASE")


#===================================================================================================
@rule("HueSwBath2003", description="Hue Bathroom dimmer Key 2 (INCREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 2003.0")
def hue_bathroom_switch2003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath3000", description="Hue Bathroom dimmer Key 3 (DECREASE) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3000.0")
def hue_bathroom_switch3000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath30012", description="Hue Bathroom dimmer Key 3 (DECREASE) - decrease brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3002.0")
def hue_bathroom_switch30012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Bathroom"]) != "OFF":
        events.sendCommand("gLight_Brightness_Bathroom", "DECREASE")


#===================================================================================================
@rule("HueSwBath3003", description="Hue Bathroom dimmer Key 3 (DECREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 3003.0")
def hue_bathroom_switch3003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath4000", description="Hue Bathroom dimmer Key 4 (OFF) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4000.0")
def hue_bathroom_switch4000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwBath4001", description="Hue Bathroom dimmer Key 4 (OFF) Hold - Turn of Bathroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4001.0")
def hue_bathroom_switch4001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Bathroom", "OFF")


#===================================================================================================
@rule("HueSwBath4002", description="Hue Bathroom dimmer Key 4 (OFF) Short Release - Turn of Bathroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4002.0")
def hue_bathroom_switch4002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Bathroom"]) != "OFF":
        events.sendCommand("Light_Scene_Bathroom", "OFF")


#===================================================================================================
@rule("HueSwBath4003", description="Hue Bathroom dimmer Key 4 (OFF) Long Release - Turn of all Bathroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_bathroom:dimmer_switch_event triggered 4003.0")
def hue_bathroom_switch4003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Bathroom", "OFF")
