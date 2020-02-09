'''
----------------------------------------------------------------------------------------------------
temperature_livingroom.py - Set avg living room temp based on Nefit Easy and Netatmo NHC.
----------------------------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX

log = logging.getLogger("{}.temp_living".format(LOG_PREFIX))

#==================================================================================================
@rule("Average Temp Livingroom", description="Calculate average livingroom temperature", tags=["sensor"])
@when("Item CV_Temp_Livingroom changed")
@when("Item NHC_Temp_Livingroom changed")
def temperatureLivingroom(event):
    temperatureLivingroom.log = logging.getLogger("{}.temperatureLivingroom".format(LOG_PREFIX))
    temperatureLivingroom.log.debug("Updating avg livingroom temp from changed [{}]".format(event.itemName))
    if ir.getItem("CV_Temp_Livingroom").state is not None:
        if ir.getItem("NHC_Temp_Livingroom").state is not None:
            events.postUpdate("Temp_Avg_Livingroom", str((float(str(ir.getItem("CV_Temp_Livingroom").state)) + float(str(ir.getItem("NHC_Temp_Livingroom").state)))/2))
        else:
            events.postUpdate("Temp_Avg_Livingroom", str(ir.getItem("CV_Temp_Livingroom").state))
    elif items.NHC_Temp_Livingroom is not None:
        events.postUpdate("Temp_Avg_Livingroom", str(ir.getItem("NHC_Temp_Livingroom").state))
    else:
        temperatureLivingroom.log.warn("Living room temp sensors are NULL")
