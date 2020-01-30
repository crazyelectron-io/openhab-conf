'''
----------------------------------------------------------------------------------------------------
power_use_total.py - Sum the Tarif 1 and Tarif 2 DSMR power meter readings.
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

#==================================================================================================
@rule("Power Use Total", description="Sum the Tarif 1 and Tarif 2 power use meter readings", tags=["energy"])
@when("Item Power_Use_T1_Total changed")
@when("Item Power_Use_T2_Total changed")
def powerUseTotal(event):
    if event.oldItemState is None:
        return

    powerUseTotal.log = logging.getLogger("{}.powerUseTotal".format(LOG_PREFIX))

    if not isinstance(ir.getItem("Power_Use_T1_Total"), UnDefType) and not isinstance(ir.getItem("Power_Use_T2_Total"), UnDefType):
        events.postUpdate("Power_Use_Total", str(float(str(ir.getItem("Power_Use_T1_Total").state)) + float(str(ir.getItem("Power_Use_T2_Total").state))))
    else:
        if isinstance(ir.getItem("Power_Use_T1_Total"), UnDefType):
            powerUseTotal.log.warn("Item [Power_Use_T1_Total] is NULL, skip DSMR readings sum update")
        if isinstance(ir.getItem("Power_Use_T2_Total"), UnDefType):
            powerUseTotal.log.warn("Item [Power_Use_T2_Total] is NULL, skip DSMR readings sum update")