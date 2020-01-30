'''
----------------------------------------------------------------------------------------------------
power_ret_total.py - Sum the Tarif 1 and Tarif 2 DSMR power return readings.
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
@rule("Power Ret Total", description="Sum the Tarif 1 and Tarif 2 power return DSRM readings", tags=["energy"])
@when("Item Power_Ret_T1_Total changed")
@when("Item Power_Ret_T2_Total changed")
def powerRetTotal(event):
    if event.oldItemState is None:
        return

    powerRetTotal.log = logging.getLogger("{}.powerRetTotal".format(LOG_PREFIX))

    if not isinstance(ir.getItem("Power_Use_T1_Total"), UnDefType) and not isinstance(ir.getItem("Power_Use_T2_Total"), UnDefType):


    if ir.getItem("Power_Ret_T1_Total").state is not None and ir.getItem("Power_Ret_T2_Total").state is not None:
        events.postUpdate("Power_Ret_Total", str(float(str(ir.getItem("Power_Ret_T1_Total").state)) + float(str(ir.getItem("Power_Ret_T2_Total").state))))
    else:
        if isinstance(ir.getItem("Power_Ret_T1_Total"), UnDefType):
            powerRetTotal.log.warn("Item [Power_Ret_T1_Total] is NULL, skip DSRM readings sum update")
        if isinstance(ir.getItem("Power_Ret_T2_Total"), UnDefType):
            powerRetTotal.log.warn("Item [Power_Ret_T2_Total] is NULL, skip DSRM readings sum update")
