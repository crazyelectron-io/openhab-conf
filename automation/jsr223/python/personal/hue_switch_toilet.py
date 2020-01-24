'''
----------------------------------------------------------------------------------------------------
hue_switch_toilet.py - Dimmer Switch toilet Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
Key 1 (ON) first press:
	Turn on toilet lighting (Scene EVENING)
Key 1 (ON) second press:
	Turn on toilet lighting (Scene READ)
Key 1 (ON) third press:
	Turn on toilet lighting (Scene BRIGHT)
Key 1 (ON) fourth press:
	TUrn on toilet lighting (Scene EVENING)
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
# from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent


log = logging.getLogger("{}.hue_toilet".format(LOG_PREFIX))


#===================================================================================================
@rule("HueSwToilet1000", description="Hue toilet dimmer Key 1 (ON) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1000.0")
def hue_toilet_switch1000(event):
    log.info("Event [{}] received".format(event.event))
    
    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet1001", description="Hue toilet dimmer Key 1 (ON) Hold - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1001.0")
def hue_toilet_switch1001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet1002", description="Hue toilet dimmer Key 1 (ON) Short release - turn off hall/kitchen light", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1002.0")
def hue_toilet_switch1002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Toilet"]) == "OFF":
        log.info("First Button 1 (ON) Short Release - Set toilet Scene to EVENING")
        events.sendCommand("Light_Scene_Toilet", "EVENING")
    elif str(items["Light_Scene_Toilet"]) == "EVENING":
        log.info("Second Button 1 (ON) Short Release - Set toilet Scene to READ")
        events.sendCommand("Light_Scene_Toilet", "READ")
    elif str(items["Light_Scene_Toilet"]) == "READ":
        log.info("Third Button 1 (ON) Short Release - Set toilet Scene to BRIGHT")
        events.sendCommand("Light_Scene_Toilet", "BRIGHT")
    else:
        log.info("Fourth Button 1 (ON) Short Release state - reset to EVENING scene")
        events.sendCommand("Light_Scene_Toilet", "EVENING")


#===================================================================================================
@rule("HueSwToilet1003", description="Hue toilet dimmer Key 1 (ON) Long release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 1003.0")
def hue_toilet_switch1003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet2000", description="Hue toilet dimmer Key 2 (INCREASE) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2000.0")
def hue_toilet_switch2000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet20012", description="Hue toilet dimmer Key 2 (INCREASE) - increase brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2002.0")
def hue_toilet_switch20012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Toilet"]) != "OFF":
        events.sendCommand("gLight_Brightness_toilet", "INCREASE")


#===================================================================================================
@rule("HueSwToilet2003", description="Hue toilet dimmer Key 2 (INCREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 2003.0")
def hue_toilet_switch2003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet3000", description="Hue toilet dimmer Key 3 (DECREASE) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3000.0")
def hue_toilet_switch3000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet30012", description="Hue toilet dimmer Key 3 (DECREASE) - decrease brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3002.0")
def hue_toilet_switch30012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Toilet"]) != "OFF":
        events.sendCommand("gLight_Brightness_toilet", "DECREASE")


#===================================================================================================
@rule("HueSwToilet3003", description="Hue toilet dimmer Key 3 (DECREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 3003.0")
def hue_toilet_switch3003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet4000", description="Hue toilet dimmer Key 4 (OFF) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4000.0")
def hue_toilet_switch4000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwToilet4001", description="Hue toilet dimmer Key 4 (OFF) Hold - Turn of toilet lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4001.0")
def hue_toilet_switch4001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Toilet", "OFF")


#===================================================================================================
@rule("HueSwToilet4002", description="Hue toilet dimmer Key 4 (OFF) Short Release - Turn of toilet lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4002.0")
def hue_toilet_switch4002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    if str(items["Light_Scene_Toilet"]) != "OFF":
        events.sendCommand("Light_Scene_Toilet", "OFF")


#===================================================================================================
@rule("HueSwToilet4003", description="Hue toilet dimmer Key 4 (OFF) Long Release - Turn of all toilet lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_toilet:dimmer_switch_event triggered 4003.0")
def hue_toilet_switch4003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Toilet", "OFF")
