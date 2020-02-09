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
from core.jsr223.scope import actions

#==================================================================================================
@rule("LGTVVolUpDn", description="Handle volume increase/decrease commands", tags=["media"])
@when("Item LGTV_VolDummy_Livingroom received command")
def lgtvVolumeUpDown(event):
    lgtvVolumeUpDown.log.info("LGTV Volume Up-Down [{}]".format(event.event))
    if event.itemState == 0:
        events.sendCommand("LGTV_Volume_Livingroom", "DECREASE")
    elif event.itemState == 1:
        events.sendCommand("LGTV_Volume_Livingroom", "INCREASE")
    else:
        lgtvVolumeUpDown.log.warn("Invalid command [{}] received".format(event.itemState))

#==================================================================================================
@rule("LGTVChannelUpDn", description="Handle channel up/down commands", tags=["media"])
@when("Item LGTV_ChannelDummy_Livingroom received command")
def lgtvChannelUpDown(event):
    lgtvChannelUpDown.log.info("LGTV Channel Up-Down [{}]".format(event.event))
    action = actions.get("lgwebos","lgwebos:WebOSTV:tvlivingroom")
    if action is None:
        lgtvChannelUpDown.log.info("LGTV.Channel.UpDn", "Actions not found (check thing ID)")
        return
    cmd = event.receivedCommand
    lgtvChannelUpDown.log.info("LGTV.Channel.UpDn", "Received command [{}]".format(cmd))
    if cmd == 0:
        action.decreaseChannel()
    elif cmd == 1:
        action.increaseChannel()
    else:
        lgtvChannelUpDown.log.warn("Invalid channle up-down command")