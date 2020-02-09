'''
----------------------------------------------------------------------------------------------------
lgtv_power.py - Handle Power On command for the LG TV (using WoL).
----------------------------------------------------------------------------------------------------
Changelog:
20200207 v02    Updated logging.
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when

#==================================================================================================
@rule("LGTVPower", description="Power on TV via Wake on LAN", tags=["media"])
@when("Item LGTV_Power_Livingroom received command ON")
def lgtvPowerOn(event):
    lgtvPowerOn.log.info("LGTV WoL Power On")
    events.sendCommand("LGTV_WoL_Livingroom", "ON")
