from core.rules import rule
from core.triggers import when
from core.metadata import get_key_value, set_metadata
from threading import Timer
from core.actions import Transformation, NotificationAction
from core.log import log_traceback

#---------------------------------------------------------------------------------------------------
# Python Timers for online alerts
alertTimers = {}


@log_traceback
def alert_timer_expired(itemName, name, origState):
    status_alert.log.debug("Status alert timer expired for {} {} {}".format(name, origState, items[itemName]))
    del alertTimers[itemName]
    if items[itemName] == origState:
        NotificationAction.sendBroadcastNotification("{} is now {}".format(name, items[itemName])) #Transformation.transform("MAP", "admin.map", str(items[itemName]))
        set_metadata(itemName, "Alert", { "alerted" : "ON"}, overwrite=False)
    else:
        status_alert.log.warn("{} is flapping!".format(itemName))


@rule("Device online/offline", description="A device we track it's online/offline status changed state", tags=["admin"])
@when("Member of gSensorStatus changed")
def status_alert(event):
    status_alert.log.info("Status alert for {} changed to {}".format(event.itemName, event.itemState))

    if isinstance(event.oldItemState, UnDefType):
        return

    alerted = get_key_value(event.itemName, "Alert", "alerted") or "OFF"
    name = get_key_value(event.itemName, "Static", "name") or event.itemName

    #If the Timer exists and the sensor changed the sensor is flapping, cancel the Timer
    if event.itemName in alertTimers:
        alertTimers[event.itemName].cancel()
        del alertTimers[event.itemName]
        status_alert.log.warning(name +  " is flapping!")
        return

    '''
    If alerted == "OFF" and event.itemName == OFF than sensor went offline and we have not yet alerted
    If alerted == "ON" and event.itemName == ON then the sensor came back online after we alerted that
    it was offline
    '''
    status_alert.log.info("Looking to see if we need to create a Timer: {} {}".format(alerted, event.itemState))
    if alerted == str(event.itemState):
        # Wait one minute before alerting to make sure it isn't flapping
        alertTimers[event.itemName] = Timer(60, lambda: alert_timer_expired(event.itemName, name, event.itemState))
        alertTimers[event.itemName].start()
