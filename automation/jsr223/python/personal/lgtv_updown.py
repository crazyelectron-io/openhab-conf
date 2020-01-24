'''
----------------------------------------------------------------------------------------------------
lgtv_updown.py - Handle VOlume and Channel Up/Down commands for LG TV.
----------------------------------------------------------------------------------------------------
Changelog:
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX


log = logging.getLogger("{}.lgtv_updown".format(LOG_PREFIX))


#==================================================================================================
@rule("LGTVVolUpDn", description="Handle volume increase/decrease commands", tags=["media"])
@when("Item LGTV_VolDummy_Livingroom received command")
def lgtv_volume_updown(event):
    log.info("LGTV Volume Up-Down [{}]".format(event.event))
    if event.itemState == 0:
        events.sendCommand("LGTV_Volume_Livingroom", "DECREASE")
    elif event.itemState == 1:
        events.sendCommand("LGTV_Volume_Livingroom", "INCREASE")
    else:
        log.warn("Invalid command [{}] received".format(event.itemState))


#==================================================================================================
@rule("LGTVChannelUpDn", description="Handle channel up/down commands", tags=["media"])
@when("Item LGTV_ChannelDummy_Livingroom received command")
def lgtv_volume_updown(event):
    log.info("LGTV Channel Up-Down [{}]".format(event.event))

    actions = getActions("lgwebos","lgwebos:WebOSTV:tvlivingroom")
    if actions is None:
        log.info("LGTV.Channel.UpDn", "Actions not found (check thing ID)")
        return

    cmd = event.receivedCommand
    log.info("LGTV.Channel.UpDn", "Received command [{}]".format(cmd))
                
    if cmd == 0:
        actions.decreaseChannel()
    elif cmd == 1:
        actions.increaseChannel()
    else:
        log.warn("Invalid channle up-down command")
