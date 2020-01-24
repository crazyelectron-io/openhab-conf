'''
----------------------------------------------------------------------------------------------------
lgtv_power.py - Handle Power On command for the LG TV.
----------------------------------------------------------------------------------------------------
Changelog:
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
This rule assumes the Wake-On-LAN binding is also installed.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX


log = logging.getLogger("{}.lgtv_power".format(LOG_PREFIX))


#==================================================================================================
@rule("LGTVPower", description="Power on TV via Wake on LAN", tags=["media"])
@when("Item LGTV_Power_Livingroom received command ON")
def lgtv_power_on(event):
    log.info("LGTV WoL Power On")
    events.sendCommand("LGTV_WoL_Livingroom", "ON")
