'''
----------------------------------------------------------------------------------------------------
energy_now_delta.py - Calculate the current delta in power consumption.
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


log = logging.getLogger("{}.pwr_nowdelta".format(LOG_PREFIX))


#===================================================================================================
@rule("DSMRNowDelta", description="Calculate the current delta in power consumption", tags=["energy"])
@when("Item Power_Use_All_Current changed")
@when("Item Power_Ret_All_Current changed")
def calc_power_delta_now(event):
    if items.Power_Ret_All_Current is not None and items.Power_Use_All_Current is not None:
        events.postUpdate("Power_Delta_All_Current", str(float(str(items.Power_Use_All_Current)) - float(float(str(items.Power_Ret_All_Current)))))
        events.sendCommand("DSMR_Watchdog", "ON")
    else:
        log.warn("[{}] not initialized, skip calculation of PowerDelta".format("Power_Ret_All_current" if items.Power_Ret_All_Current is None else items.Power_Use_All_Current))


#===================================================================================================
@rule("DSMRPhaseDelta", description="Calculate delta power per phase", tags=["energy"])
@when("Item Power_Ret_L1_Current changed")
@when("Item Power_Use_L1_Current changed")
@when("Item Power_Ret_L2_Current changed")
@when("Item Power_Use_L2_Current changed")
@when("Item Power_Ret_L3_Current changed")
@when("Item Power_Use_L3_Current changed")
def calc_power_phases_now(event):
    phase = event.itemName.split("_")[2]

    ItemPwrRet = ir.getItem("Power_Ret_" + phase + "_Current")
    ItemPwrUse = ir.getItem("Power_Use_" + phase + "_Current") 
    ItemPwrDelta = ir.getItem("Power_Delta_" + phase + "_Current")

    if ItemPwrRet.state is not None and ItemPwrUse.state is not None:
        events.postUpdate(ItemPwrDelta.name, str(float(str(ItemPwrUse.state)) - float(str(ItemPwrRet.state))))
    else:
        log.warn("[{}] not initialzed, skip [Power_Delta_{}_Current] calculation".format(ItemPwrRet.name if ItemPwrRet.state is None else ItemPwrUse.name, phase))
