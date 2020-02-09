'''
----------------------------------------------------------------------------------------------------
power_delta_now.py - Calculate the current delta in total power consumption.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX

#===================================================================================================
@rule("DSMRNowDelta", description="Calculate the current delta in total power consumption", tags=["energy"])
@when("Item Power_Use_All_Current changed")
@when("Item Power_Ret_All_Current changed")
def powerDeltaNow(event):
    if event.oldItemState is None:
        return
    if not isinstance(ir.getItem("Power_Ret_All_Current"), UnDefType) and not isinstance(ir.getItem("Power_Use_All_Current"), UnDefType):
        events.postUpdate("Power_Delta_All_Current", str(float(str(items["Power_Use_All_Current"])) - float(str(items["Power_Ret_All_Current"]))))
        events.sendCommand("DSMR_Watchdog", "ON")
    else:
        powerDeltaNow.log.warn("[{}] not initialized, skip calculation of PowerDelta".format("Power_Ret_All_current" if isinstance(ir.getItem("Power_Ret_All_Current"), UnDefType) else items["Power_Use_All_Current"]))