'''
----------------------------------------------------------------------------------------------------
watchdog.py - Monitor status of bindings and sensors.
----------------------------------------------------------------------------------------------------
20200229 v01    Initial version
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
try:
    from org.openhab.core.thing import ThingUID
except:
    from org.eclipse.smarthome.core.thing import ThingUID
from core.log import log_traceback
from core.actions import LogAction, NotificationAction, Exec, ScriptExecution
from core.items import add_item,remove_item
from org.joda.time import DateTime


keyThingsDict = {
    # SolarEdge API Binding
    "solaredge:generic:se7k": {
        "thing_name": "SolarEdge API Binding",
        "status_item": "SolarEdge_API_Status",
        "restart_info": {
            "binding_uri": "org.openhab.binding.solaredge",
            "wait_time": 600,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        },
        "watchdog_item": "SolarEdge_Watchdog",
        "watchdog_items": ["Power_Use_All_Current",],
        "watchdog_time": 1800,
    },
    # Netatmo Healthy Home Coach Binding
    "netatmo:netatmoapi:home": {
        "thing_name": "Netatmo Healthy Coach (Livingroom)",
        "status_item": "NHC_API_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.netatmo",
            "wait_time": 600,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        }
    },
    # Daikin Thing Bedroom
    "daikin:ac_unit:192_168_2_135": {
        "thing_name": "Daiking Airco (Bedroom)",
        "status_item": "AC_Bedroom_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.daikin",
            "wait_time": 120,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        }
    },
    # Daikin Thing Stephan
    "daikin:ac_unit:192_168_2_125": {
        "thing_name": "Daiking Airco (Stephan)",
        "status_item": "AC_Laundry_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.daikin",
            "wait_time": 300,
            "reschedule_timer_on_update": True,
            "notify_restart": False,
        }
    },
    # Daikin Thing Menno
    "daikin:ac_unit:192_168_2_160": {
        "thing_name": "Daiking Airco (Menno)",
        "status_item": "AC_Guestroom_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.daikin",
            "wait_time": 300,
            "reschedule_timer_on_update": True,
            "notify_restart": False,
        }
    },
    # Daikin Thing Study
    "daikin:ac_unit:192_168_2_137": {
        "thing_name": "Daiking Airco (Study)",
        "status_item": "AC_Study_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.daikin",
            "wait_time": 300,
            "reschedule_timer_on_update": True,
            "notify_restart": False,
        }
    },
    # HUE Binding
    "hue:bridge:0017882ec5b3": {
        "thing_name": "HUE Gateway",
        "status_item": "HUE_Gateway_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.hue",
            "wait_time": 30,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        },
    },
    # Verisure Thing
    "verisure:bridge:myverisure": {
        "thing_name": "VeriSure binding",
        "status_item": "VeriSure_API_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.verisure",
            "wait_time": 180,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        },
    },
    # MQTT Broker Thing
    "mqtt:broker:mosquitto": {
        "thing_name": "MQTT Broker binding",
        "status_item": "MQTT_Broker_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.mqtt",
            "wait_time": 60,
            "reschedule_timer_on_update": True,
            "notify_rerstart": True,
        },
    },
    # Volvo V90 VoC Thing
    "volvooncall:vehicle:v90:V90": {
        "thing_name": "V90 Broker binding",
        "status_item": "V90_VoC_Status",
        "watched_items": ["xxx"],
        "restart_info": {
            "binding_uri": "org.openhab.binding.volvooncall",
            "wait_time": 600,
            "reschedule_timer_on_update": True,
            "notify_rerstart": True,
        },
    },
}


import pprint
pp = pprint.PrettyPrinter(indent=4)

rule_init_timestamp = DateTime.now()
logTitle = "watchdog.py@{ts}".format(ts=rule_init_timestamp.toString("HH:mm:ss"))
ruleTimeStamp = " -- (Rule set initialised {} at {})".format(
    rule_init_timestamp.toString("E d MMM yyyy"),
    rule_init_timestamp.toString("HH:mm:ss (z)")
)
rulePrefix = "Watchdog | "

# Group name for all watchdog items
WATCHDOG_GROUP = "gWatchdog"

# Binding restart timers
timers = {}
# Binding restart counters
binding_restarts = {}


#---------------------------------------------------------------------------------------------------
# For testing purposes only: Use this to remove created items
@log_traceback
def removeWatchdogItems():
    for item in ir.getItemsByTag("Watchdog"):
        LogAction.logInfo(logTitle, u"Remove Watchdog Item [{}]".format(item.name))
        remove_item(item)
    remove_item(WATCHDOG_GROUP)


#---------------------------------------------------------------------------------------------------
def addWatchdogItems():
    """
    Create the Watchdog Items and Group if they don't exist yet.
    """
    global logTitle

    # Add Watchdog Group if it doesn't exist
    if ir.getItems(WATCHDOG_GROUP) == []:
        LogAction.logInfo(logTitle, u"Create Group [{}]".format(WATCHDOG_GROUP))
        add_item(WATCHDOG_GROUP, item_type="Group", label="Watchdog Items Group", tags=["Watchdog"])
    try:
        for entry in keyThingsDict.values():
            wdItemName = entry.get("status_item")
            if ir.getItems(wdItemName) == []:
                add_item(wdItemName, item_type="String", groups=[WATCHDOG_GROUP], label=entry.get("thing_name"), tags=["Watchdog"])
                LogAction.logInfo(logTitle, u"Created item [{}] in Group [{}]".format(wdItemName, WATCHDOG_GROUP))
    except:
        import traceback
        LogAction.logError(logTitle, u"{}".format(traceback.format_exc()))


#---------------------------------------------------------------------------------------------------
def scriptLoaded(id_):
    # removeWatchdogItems()        # *For testing purposes only*
    addWatchdogItems()


#---------------------------------------------------------------------------------------------------
def schedule_binding_restart(
    binding_id,
    binding_name,
    binding_thing_name, 
    delay_seconds,
    reschedule_timer_on_update=False,
    notify_restart=False
):
    """
    Schedule a binding restart if needed (if Thing status is not 'ONLINE')
    
    Arguments:
        binding_id {String} - The binding identifier (e.g. 'org.openhab.binding.xyzzy')
        binding_name {String} - The name of the binding, e.g. 'XYZZY'
        binding_thing_name {String} - The Thing name linked to the binding (e.g. binding:id:x:y:z)
        delay_seconds {Integer} - # seconds to wait before restarting the binding
    Keyword Arguments:
        reschedule_timer_on_update {bool} - Reschedule restart if update received
        notify_restart {bool} - Notify if the binding is scheduled for restarting
    """
    global timers
    global binding_restarts

    if delay_seconds < 0:
        delay_seconds = 0

    # First, check if Thing is already back online
    current_state = str(things.get(ThingUID(binding_thing_name)).status)
    if current_state == "ONLINE":
        if timers.get(binding_id):
            timers[binding_id].cancel()
            timers[binding_id] = None
            LogAction.logInfo(logTitle, u"No need to restart {} ({} back online)".format(binding_name, binding_thing_name))
        return

    if timers.get(binding_id) is None:
        if notify_restart is True:
            NotificationAction.sendBroadcastNotification(u"Restart scheduled for {} in {}s (status={})".format(binding_name, delay_seconds, current_state))
        # Define the call-back that will be executed when the timer expires.
        def cb():
            global logTitle
            current_state = str(things.get(ThingUID(binding_thing_name)).status)
            if current_state == "ONLINE":
                LogAction.logInfo(logTitle, u"No need to restart {} (status={})".format(binding_name, current_state))
                if notify_restart is True:
                    NotificationAction.sendBroadcastNotification(u"Auto restart canceled for {} (status={})".format(binding_name, current_state))
            else:
                LogAction.logInfo(logTitle, u"Will now restart {} (status={})".format(binding_name, current_state))
                # Keep track of binding restarts
                restart_counter = binding_restarts.get(binding_id)
                if restart_counter is None:
                    binding_restarts[binding_id] = 1
                else:
                    binding_restarts[binding_id] = int(restart_counter) + 1

                if notify_restart is True:
                    NotificationAction.sendBroadcastNotification(u"Auto restart of {} (status={})".format(binding_name, current_state))
                # Restart the binding (use the 'openhab-karaf' entry in ssh config file)
                Exec.executeCommandLine("/bin/sh@@-c@@ssh openhab-karaf 'bundle:restart {}'".format(binding_id))
            timers[binding_id] = None

        timers[binding_id] = ScriptExecution.createTimer(DateTime.now().plusSeconds(delay_seconds), cb)

    else:
        if reschedule_timer_on_update is True:
            LogAction.logInfo(logTitle, u"Reschedule '{}' binding restart (status='{}').".format(binding_name, current_state))
            timers.get(binding_id).reschedule(DateTime.now().plusSeconds(delay_seconds))


#---------------------------------------------------------------------------------------------------
# Automatically add the needed decorators for all monitored Things in things_dict
def key_things_trigger_generator_thing_changed(things_dict):
    def generated_triggers(function):
        global logTitle
        for k in keyThingsDict.keys():
            logPrefix = u"generated_triggers(): adding @when(\"Thing {} changed\") trigger for {}".format(k, unicode(keyThingsDict.get(k).get("thing_name")))
            LogAction.logInfo(logTitle, logPrefix)
            when("Thing {} changed".format(k))(function)
        return function

    return generated_triggers


#===================================================================================================
@rule(rulePrefix+"Thing status update", description=u"Update Thing-proxy items with status"+ruleTimeStamp, tags=["watchdog", ruleTimeStamp])
@when("Time cron 0 0/10 * * * ?")
@key_things_trigger_generator_thing_changed(keyThingsDict)
def Rule_KeyThingStatusUpdate(event):
    global logTitle
    global keyThingsDict
    logPrefix = "Rule_KeyThingStatusUpdate(): "
    LogAction.logDebug(logTitle, logPrefix + "event = " + pp.pformat(event))

    keyThings = []
    if event:
        keyThings.append(str(event.thingUID))
    else:
        for k in keyThingsDict.keys():
            keyThings.append(k)

    for k in keyThings:
        keyItemInfo = keyThingsDict[k]
        keyStatusItem = keyItemInfo.get("status_item")
        keyStatusItemThingName = keyItemInfo.get("thing_name")
        bindingRestartInfo = keyItemInfo.get("restart_info")
        nodeName = k.split(":")[-1]
        # thing state is not available in event if rule triggered by cron:
        if event:
            nodeState = str(event.statusInfo)
            LogAction.logInfo(logTitle, logPrefix+"Thing {} ({}, status item {}) status changed to {}".format(nodeName, keyStatusItemThingName, keyStatusItem, nodeState))
        else:
            nodeState = things.get(ThingUID(k)).status
        events.postUpdate(keyStatusItem, str(nodeState))

        # Restart some bindings if needed
        if bindingRestartInfo:
            LogAction.logDebug(logTitle, logPrefix+u"Restart {} (URI {}) if offline; current status is {}".format(keyStatusItemThingName, bindingRestartInfo.get("binding_uri"), nodeState))
            # Note: schedule_binding_restart() takes care of managing the Thing status
            schedule_binding_restart(
                bindingRestartInfo.get("binding_uri"),
                keyStatusItemThingName,
                k,
                bindingRestartInfo.get("wait_time"),
                reschedule_timer_on_update=bindingRestartInfo.get("reschedule_timer_on_update", False),
                notify_restart=bindingRestartInfo.get("notify_restart", False)
            )
