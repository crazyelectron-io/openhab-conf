'''
----------------------------------------------------------------------------------------------------
energy_tariffs.py - Sum the Tarif 1 and Tarif 2 DSMR power meter readings.
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

log = logging.getLogger("{}.dsmr_total".format(LOG_PREFIX))

#==================================================================================================
@rule("DSMRUseSum", description="Sum the Tarif 1 and Tarif 2 power use meter readings", tags=["energy"])
@when("Item Power_Use_T1_Total changed")
@when("Item Power_Use_T2_Total changed")
def calc_power_use_total(event):
    if items.Power_Use_T1_Total is not None and items.Power_Use_T2_Total is not None:
        events.postUpdate("Power_Use_Total", str(float(str(items.Power_Use_T1_Total)) + float(str(items.Power_Use_T2_Total))))
    else:
        if items.Power_Use_T1_Total is None:
            log.warn("Item 'Power_Use_T1_Total' is NULL, skip tarif meter readings sum update")
        if items.Power_Use_T2_Total is None:
            log.warn("Item 'Power_Use_T2_Total' is NULL, skip tarif meter readings sum update")

#==================================================================================================
@rule("DSMRRetSum", description="Sum the Tarif 1 and Tarif 2 power return meter readings", tags=["energy"])
@when("Item Power_Ret_T1_Total changed")
@when("Item Power_Ret_T2_Total changed")
def calc_power_ret_total(event):
    if items.Power_Ret_T1_Total is not None and items.Power_Ret_T2_Total is not None:
        events.postUpdate("Power_Ret_Total", str(float(str(items.Power_Ret_T1_Total)) + float(str(items.Power_Ret_T2_Total))))
    else:
        if items.Power_Ret_T1_Total is None:
            log.warn("Item 'Power_Ret_T1_Total' is NULL, skip tarif meter readings sum update")
        if items.Power_Ret_T2_Total is None:
            log.warn("Item 'Power_Ret_T2_Total' is NULL, skip tarif meter readings sum update")
