from core.rules import rule
from core.triggers import when
from org.eclipse.smarthome.core.thing import ThingUID

from core.actions import LogAction
from core.actions import NotificationAction
from core.actions import Exec
from core.actions import ScriptExecution

from org.joda.time import DateTime

keyThingsDict = {
    # SolarEdge API Binding
    "solaredge:generic:se7k": {
        "thing_name": "SolarEdge API Binding",
        "status_item": "SolarEdge_API_Status",
        "restart_info": {
            "binding_uri": "org.openhab.binding.solaredge",
            "wait_time": 300,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        }
    },
    # Netatmo Healthy Home Coach Binding
    "netatmo:netatmoapi:home": {
        "thing_name": "Netatmo Healthy Coach (Livingroom)",
        "status_item": "NHC_API_Status",
        "restart_info": {
            "binding_uri": "org.openhab.binding.netatmo",
            "wait_time": 300,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        }
    },
    # Daikin Binding
    "daikin:ac_unit:192_168_2_135": {
        "thing_name": "Daiking Airco (Bedroom)",
        "restart_info": {
            "binding_uri": "org.openhab.binding.daikin",
            "wait_time": 120,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        }
    },
    # HUE Binding
    "hue:bridge:0017882ec5b3": {
        "thing_name": "HUE Gateway",
        "status_item": "HUE_Gateway_Status",
        "restart_info": {
            "binding_uri": "org.openhab.binding.hue",
            "wait_time": 30,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        },
    },
    # Verisure Binding
    "verisure:bridge:myverisure": {
        "thing_name": "VeriSure binding",
        "status_item": "VeriSure_API_Status",
        "restart_info": {
            "binding_uri": "org.openhab.binding.verisure",
            "wait_time": 120,
            "reschedule_timer_on_update": True,
            "notify_restart": True,
        },
    },
    # MQTT Broker Binding
    "mqtt:broker:mosquitto": {
        "thing_name": "MQTT Broker binding",
        "status_item": "MQTT_Broker_Status",
        "restart_info": {
            "binding_uri": "org.openhab.binding.mqtt",
            "wait_time": 60,
            "reschedule_timer_on_update": True,
            "notify_rerstart": True,
        },
    },
}

import pprint

pp = pprint.PrettyPrinter(indent=4)

rule_init_timestamp = DateTime.now()
logTitle = "watchdog.py@{ts}".format(ts=rule_init_timestamp.toString("HH:mm:ss"))
ruleTimeStamp = " -- (Rule set initialised {date} at {ts})".format(
    date=rule_init_timestamp.toString("E d MMM yyyy"),
    ts=rule_init_timestamp.toString("HH:mm:ss (z)"),
)
rulePrefix = "Watchdog | "

# Binding restart timers
timers = {}
# Binding restart counters
binding_restarts = {}


def schedule_binding_restart(
    binding_id,
    binding_name,
    binding_thing_name,
    delay_seconds,
    reschedule_timer_on_update=False,
    notify_restart=False,
):
    """Schedule a binding restart if needed (if the Thing status differs from 'ONLINE')
    
    Arguments:
        binding_id {String} -- The binding identifier, e.g. 'org.openhab.binding.xyzzy'
        binding_name {String} -- The name of the binding, e.g. 'XYZZY'
        binding_thing_name {String} -- The Thing name linked to the binding, e.g. 'binding:id:x:y:z'
        delay_seconds {Integer} -- Number of seconds to wait before restarting the binding
    
    Keyword Arguments:
        reschedule_timer_on_update {bool} -- If a status update is received, reschedule the restart timer (default = False)
        notify_restart {bool} -- Issue a notification if the binding is scheduled for restarting (default = False)
    """
    global timers
    global binding_restarts

    if delay_seconds < 0:
        delay_seconds = 0

    current_state = str(things.get(ThingUID(binding_thing_name)).status)
    if current_state == "ONLINE":
        if timers.get(binding_id):
            timers[binding_id].cancel()
            timers[binding_id] = None
        return

    if timers.get(binding_id) is None:
        if notify_restart is True:
            NotificationAction.sendBroadcastNotification(
                u"Automatic binding restart scheduled for '{binding_name}' binding in {delay_seconds} seconds (current status of binding ID '{binding_id}' is '{state}')".format(
                    binding_id=binding_id,
                    binding_name=binding_name,
                    delay_seconds=delay_seconds,
                    state=current_state,
                ),
            )
        # Define the call-back that will be executed when the timer expires
        def cb():
            global logTitle
            current_state = str(things.get(ThingUID(binding_thing_name)).status)
            if current_state == "ONLINE":
                LogAction.logInfo(
                    logTitle,
                    u"No need to restart '{binding_name}' binding (Thing UID = '{thing_uid}', current status is '{state}').".format(
                        binding_name=binding_name,
                        thing_uid=binding_thing_name,
                        state=current_state,
                    ),
                )
                if notify_restart is True:
                    NotificationAction.sendBroadcastNotification(
                        u"Automatic binding restart cancelled for '{binding_name}' binding (Thing UID = '{thing_uid}', current status is '{state}')".format(
                            binding_name=binding_name,
                            thing_uid=binding_thing_name,
                            state=current_state,
                        ),
                    )
            else:
                LogAction.logInfo(
                    logTitle,
                    u"Will now restart '{binding_name}' binding (Thing UID = '{thing_uid}', current status is '{state}').".format(
                        binding_name=binding_name,
                        thing_uid=binding_thing_name,
                        state=current_state,
                    ),
                )
                # Keep track of binding restarts
                restart_counter = binding_restarts.get(binding_id)
                if restart_counter is None:
                    binding_restarts[binding_id] = 1
                else:
                    binding_restarts[binding_id] = int(restart_counter) + 1

                if notify_restart is True:
                    NotificationAction.sendBroadcastNotification(
                        u"Automatic binding restart of '{binding_name}' binding (Thing UID = '{thing_uid}', current status is '{state}')".format(
                            binding_name=binding_name,
                            thing_uid=binding_thing_name,
                            state=current_state,
                        ),
                    )
                # Restart the binding
                Exec.executeCommandLine(
                    "/bin/sh@@-c@@ssh -p 8101 -l openhab 192.168.2.2 -i /openhab/karaf_key 'bundle:restart {binding_id}'".format(
                        binding_id=binding_id
                    )
                )
            timers[binding_id] = None

        timers[binding_id] = ScriptExecution.createTimer(
            DateTime.now().plusSeconds(delay_seconds), cb
        )

    else:
        if reschedule_timer_on_update is True:
            LogAction.logInfo(
                logTitle,
                u"Reschedule '{binding_name}' binding restart timer (Thing UID = '{thing_uid}', current status is '{state}').".format(
                    binding_name=binding_name,
                    thing_uid=binding_thing_name,
                    state=current_state,
                ),
            )
            timers.get(binding_id).reschedule(DateTime.now().plusSeconds(delay_seconds))


# Automatically add the needed decorators for all monitored Things in things_dict (keyThingsDict)
def key_things_trigger_generator_thing_changed(things_dict):
    def generated_triggers(function):
        global logTitle
        for k in keyThingsDict.keys():
            logPrefix = u"generated_triggers(): adding @when(\"Thing '{}' changed\") trigger for '{}'".format(
                k, unicode(keyThingsDict.get(k).get("thing_name"))
            )
            LogAction.logInfo(logTitle, logPrefix)
            when("Thing '{}' changed".format(k))(function)
        return function

    return generated_triggers


@rule(
    rulePrefix + "Key thing status update",
    description=u"This rule will update Thing-based proxy items to report the status of key Things. Please note that every Thing must be defined in keyThingsDict for the rule to work."
    + ruleTimeStamp,
    tags=["watchdog", ruleTimeStamp],
)
@when("Time cron 0 0/10 * * * ?")
@key_things_trigger_generator_thing_changed(keyThingsDict)
def Rule_KeyThingStatusUpdate(event):
    global logTitle
    global keyThingsDict
    logPrefix = "Rule_KeyThingStatusUpdate(): "

    LogAction.logInfo(logTitle, logPrefix + "event = " + pp.pformat(event))

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
        nodeState = str(event.statusInfo) if event else things.get(ThingUID(k)).status
        LogAction.logInfo(
            logTitle,
            logPrefix
            + "Thing '{node_name}' ({name} with status item {item_name}) status changed to '{node_state}'".format(
                node_name=nodeName,
                name=keyStatusItemThingName,
                item_name=keyStatusItem,
                node_state=nodeState,
            ),
        )
        events.postUpdate(keyStatusItem, str(nodeState))

        # Restart some bindings if needed
        if bindingRestartInfo:
            LogAction.logInfo(
                logTitle,
                logPrefix
                + u"Will attempt restarting '{}' binding with URI '{}' if offline - current status is {}".format(
                    keyStatusItemThingName,
                    bindingRestartInfo.get("binding_uri"),
                    nodeState,
                ),
            )
            # Note: schedule_binding_restart() takes care of managing the Thing status, so don't do it here:
            schedule_binding_restart(
                bindingRestartInfo.get("binding_uri"),
                keyStatusItemThingName,
                k,
                bindingRestartInfo.get("wait_time"),
                reschedule_timer_on_update=bindingRestartInfo.get(
                    "reschedule_timer_on_update", False
                ),
                notify_restart=bindingRestartInfo.get("notify_restart", False),
            )
