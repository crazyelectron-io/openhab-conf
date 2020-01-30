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

#===================================================================================================
@rule("DSMRPhaseDelta", description="Calculate current delta power per phase", tags=["energy"])
@when("Item Power_Ret_L1_Current changed")
@when("Item Power_Use_L1_Current changed")
@when("Item Power_Ret_L2_Current changed")
@when("Item Power_Use_L2_Current changed")
@when("Item Power_Ret_L3_Current changed")
@when("Item Power_Use_L3_Current changed")
def powerPhasesNow(event):
    if event.oldItemState is None:
        return

    powerPhasesNow.log = logging.getLogger("{}.powerPhasesNow".format(LOG_PREFIX))

    phase = event.itemName.split("_")[2]

    ItemPwrRet = ir.getItem("Power_Ret_" + phase + "_Current")
    ItemPwrUse = ir.getItem("Power_Use_" + phase + "_Current") 
    ItemPwrDelta = ir.getItem("Power_Delta_" + phase + "_Current")

    if not isinstance(ItemPwrRet, UnDefType) and not isinstance(ItemPwrUse, UnDefType):
        events.postUpdate(ItemPwrDelta.name, str(float(str(ItemPwrUse.state)) - float(str(ItemPwrRet.state))))
    else:
        powerPhasesNow.log.warn("[{}] not initialzed, skip [Power_Delta_{}_Current] calculation".format(ItemPwrRet.name if ItemPwrRet.state is None else ItemPwrUse.name, phase))
