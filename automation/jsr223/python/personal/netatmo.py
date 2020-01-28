'''
----------------------------------------------------------------------------------------------------
netatmo.py - handle Netatmo Healthy Home Coach Item updates and CO2 level checks.
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
def get_co2_thresholds():
    return

#===================================================================================================
@rule("NetatmoOffline", description="Netatmo API watchdog timeout triggered (30m)", tags=["sensor"])
@when("Item NHC_Watchdog changed")
def netatmo_timeout(event):
    #--- Send a push notification to the user
    msg = "Netatmo Healthy Home Coach is not responding, please check the status of the device and online API."
    log.warning(msg)
    NotificationAction.sendBroadcastNotification(msg)
    #Echo_TTS_Livingroom.sendCommand("The " + msg)
    events.sendCommand("NHC_Watchdog", "ON")


#===================================================================================================
@rule("NetatmoCO2Check", description="Set CO2Reported switch if CO2 level above high treshold; reset if below low threshold", tags=["sensor"])
@when("Item NHC_CO2_Livingroom changed")
def netatmo_co2_check(event):
    global CO2ThresholdHi
    global CO2ThresholdLo
    global CO2HiReportedToday

    msg = ""

    if event.itemState is None:
        log.warn("Item [{}] state is NULL, exit rule".format(event.itemName))
        return
    else:
        events.sendCommand("NHC_Watchdog", "ON")
    if event.oldItemState is None:
        return

    #--- Get the current CO2 level in the livingroom, rounded to the lower 100's
    currentCO2level = (int(str(event.itemState))/100)*100

    #--- Check if CO2 level is above high threshold
    if currentCO2level > CO2ThresholdHi:
        log.info("CO2 level is above threshold [{}]".format(CO2ThresholdHi))

        # Check if not yet reported in the last hour
        if items["CO2HighReported_Livingroom"] is None or items["CO2HighReported_Livingroom"] == OFF:
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
        log.debug("CO2 level is below threshold [{}]".format(CO2ThresholdLo))
        # Check if high CO2 level has been reported today, and low level not yet reported
        if CO2HiReportedToday and (items["CO2LowReported_Livingroom"] is None or str(items["CO2LowReported_Livingroom"]) == "OFF"):
            msg = "Current CO2 level in the livingroom has returned to a healthy level of about " + str(currentCO2level) + "."
            #Echo_TTS_Livingroom.sendCommand("Hi, the "+ msg)
            NotificationAction.sendBroadcastNotification(msg)
            # LGTV_Toast_Livingroom.sendCommand(msg)
            events.postUpdate("CO2LowReported_Livingroom", "ON")

        events.postUpdate("CO2HighReported_Livingroom", "OFF")
        CO2HiReportedToday = False
    else:
        log.debug("CO2 level [{}] is above low threshold [{}] and below high threshold [{}]".format(currentCO2level, CO2ThresholdLo, CO2ThresholdHi))
 