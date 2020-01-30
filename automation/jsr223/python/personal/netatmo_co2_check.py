'''
----------------------------------------------------------------------------------------------------
netatmo_co2_check.py - Netatmo Healthy Home Coach CO2 level checks.
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
# import datetime
# from org.joda.time import DateTime
from core.actions import NotificationAction

log = logging.getLogger("{}.netatmo".format(LOG_PREFIX))

CO2ThresholdHi = 1700                # Threshold for reporting high CO2 level (ppm)
CO2ThresholdLo = 950                 # Threshold for reset high CO2 level (ppm)
CO2HiReportedToday = False           # CO2 Hi already reported today flag

#---------------------------------------------------------------------------------------------------
# TODO: Get thresholds from metadata
def getCO2Thresholds():
    return


#===================================================================================================
@rule("NetatmoCO2Check", description="Set CO2Reported switch if CO2 level above high treshold; reset if below low threshold", tags=["sensor"])
@when("Item NHC_CO2_Livingroom changed")
def netatmoCO2Check(event):
    global CO2ThresholdHi
    global CO2ThresholdLo
    global CO2HiReportedToday

    if event.oldItemState is None:
        return

    netatmoCO2Check.log = logging.getLogger("{}.netatmoCO2Check".format(LOG_PREFIX))

    msg = ""

    if event.itemState is None:
        netatmoCO2Check.log.warn("Item [{}] state is NULL, exit rule".format(event.itemName))
        return
    else:
        events.sendCommand("NHC_Watchdog", "ON")
    if event.oldItemState is None:
        return

    #--- Get the current CO2 level in the livingroom, rounded to the lower 100's
    currentCO2level = (int(str(event.itemState))/100)*100

    #--- Check if CO2 level is above high threshold
    if currentCO2level > CO2ThresholdHi:
        netatmoCO2Check.log.info("CO2 level is above threshold [{}]".format(CO2ThresholdHi))

        # Check if not yet reported in the last hour
        if ir.getItem("CO2HighReported_Livingroom").state is None or ir.getItem("CO2HighReported_Livingroom").state == OFF:
            if not CO2HiReportedToday:
                msg = "Current CO2 level in the livingroom is more than " + str(currentCO2level) + ". I suggest to open some ventilation."
            else:
                msg = "CO2 level in the livingroom is still too high at more than " + str(currentCO2level)
            NotificationAction.sendBroadcastNotification(msg)
            # Echo_TTS_Livingroom.sendCommand("Hi, the " + msg)
            # LGTV_Toast_Livingroom.sendCommand(msg)
            events.postUpdate("CO2HighReported_Livingroom", "ON")
            events.postUpdate("CO2LowReported_Livingroom", "OFF")
            CO2HiReportedToday = True

    #--- Check if CO2 level below low threshold
    elif currentCO2level < CO2ThresholdLo:
        netatmoCO2Check.log.debug("CO2 level is below threshold [{}]".format(CO2ThresholdLo))
        # Check if high CO2 level has been reported today, and low level not yet reported
        if CO2HiReportedToday and (ir.getItem("CO2LowReported_Livingroom").state is None or str(ir.getItem("CO2LowReported_Livingroom").state) == "OFF"):
            msg = "Current CO2 level in the livingroom has returned to a healthy level of about " + str(currentCO2level) + "."
            #Echo_TTS_Livingroom.sendCommand("Hi, the "+ msg)
            NotificationAction.sendBroadcastNotification(msg)
            # LGTV_Toast_Livingroom.sendCommand(msg)
            events.postUpdate("CO2LowReported_Livingroom", "ON")

        events.postUpdate("CO2HighReported_Livingroom", "OFF")
        CO2HiReportedToday = False
    else:
        netatmoCO2Check.log.debug("CO2 level [{}] is above low threshold [{}] and below high threshold [{}]".format(currentCO2level, CO2ThresholdLo, CO2ThresholdHi))
 