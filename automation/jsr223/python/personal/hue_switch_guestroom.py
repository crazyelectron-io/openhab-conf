'''
----------------------------------------------------------------------------------------------------
hue_switch_Guestroom.py - Dimmer Switch Guest room Buttons handling rule.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
Key 1 (ON) first press:
	Turn on guestroom lighting (Scene EVENING)
Key 1 (ON) second press:
	Turn on guestroom lighting (Scene READ)
Key 1 (ON) third press:
	Turn on guestroom lighting (Scene BRIGHT)
Key 1 (ON) fourth press:
	TUrn on guestroom lighting (Scene EVENING)
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX

log = logging.getLogger("{}.hue_Guestroom".format(LOG_PREFIX))

#===================================================================================================
@rule("HueSwGuest1000", description="Hue guestroom dimmer Key 1 (ON) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 1000.0")
def hue_Guestroom_switch1000(event):
    log.info("Event [{}] received".format(event.event))
    
    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest1001", description="Hue guestroom dimmer Key 1 (ON) Hold - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 1001.0")
def hue_Guestroom_switch1001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
#
@rule("HueSwGuest1002", description="Hue guestroom dimmer Key 1 (ON) Short release - turn off hall/kitchen light", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 1002.0")
def hue_Guestroom_switch1002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if str(ir.getItem("Light_Scene_Guestroom").state) == "OFF":
        log.info("First Button 1 (ON) Short Release - Set guestroom Scene to EVENING")
        events.sendCommand("Light_Scene_Guestroom", "EVENING")
    elif str(ir.getItem("Light_Scene_Guestroom").state) == "EVENING":
        log.info("Second Button 1 (ON) Short Release - Set guestroom Scene to READ")
        events.sendCommand("Light_Scene_Guestroom", "READ")
    elif str(ir.getItem("Light_Scene_Guestroom").state) == "READ":
        log.info("Third Button 1 (ON) Short Release - Set guestroom Scene to BRIGHT")
        events.sendCommand("Light_Scene_Guestroom", "BRIGHT")
    else:
        log.info("Fourth Button 1 (ON) Short Release state - reset to EVENING scene")
        events.sendCommand("Light_Scene_Guestroom", "EVENING")


#===================================================================================================
@rule("HueSwGuest1003", description="Hue guestroom dimmer Key 1 (ON) Long release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 1003.0")
def hue_Guestroom_switch1003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest2000", description="Hue guestroom dimmer Key 2 (INCREASE) Initial Press - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 2000.0")
def hue_Guestroom_switch2000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest20012", description="Hue guestroom dimmer Key 2 (INCREASE) - increase brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 2001.0")
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 2002.0")
def hue_Guestroom_switch20012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if ir.getItem("Light_Scene_Guestroom != OFF").state:
        events.sendCommand("gLight_Brightness_Guestroom", "INCREASE")


#===================================================================================================
@rule("HueSwGuest2003", description="Hue guestroom dimmer Key 2 (INCREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 2003.0")
def hue_Guestroom_switch2003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest3000", description="Hue guestroom dimmer Key 3 (DECREASE) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 3000.0")
def hue_Guestroom_switch3000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest30012", description="Hue guestroom dimmer Key 3 (DECREASE) - decrease brightness", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 3001.0")
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 3002.0")
def hue_Guestroom_switch30012(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    if ir.getItem("Light_Scene_Guestroom != OFF").state:
        events.sendCommand("gLight_Brightness_Guestroom", "DECREASE")


#===================================================================================================
@rule("HueSwGuest3003", description="Hue guestroom dimmer Key 3 (DECREASE) Long Release - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 3003.0")
def hue_Guestroom_switch3003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest4000", description="Hue guestroom dimmer Key 4 (OFF) Initial Pressed - ignored", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 4000.0")
def hue_Guestroom_switch4000(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))


#===================================================================================================
@rule("HueSwGuest4001", description="Hue guestroom dimmer Key 4 (OFF) Hold - Turn of guestroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 4001.0")
def hue_Guestroom_switch4001(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Guestroom", "OFF")


#===================================================================================================
@rule("HueSwGuest4002", description="Hue guestroom dimmer Key 4 (OFF) Short Release - Turn of guestroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 4002.0")
def hue_Guestroom_switch4002(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3].split("_")[1]
    log.info("Switch detected [{}]".format(switch))

    if str(ir.getItem("Light_Scene_Guestroom").state) != "OFF":
        events.sendCommand("Light_Scene_Guestroom", "OFF")


#===================================================================================================
@rule("HueSwGuest4003", description="Hue guestroom dimmer Key 4 (OFF) Long Release - Turn of all guestroom lighting", tags=["lights"])
@when("Channel hue:0820:0017882ec5b3:dim_guest:dimmer_switch_event triggered 4003.0")
def hue_Guestroom_switch4003(event):
    log.info("Event [{}] received".format(event.event))

    switch = str(event.channel).split(":")[3]
    log.info("Switch detected [{}]".format(switch))

    events.sendCommand("Light_Scene_Guestroom", "OFF")
