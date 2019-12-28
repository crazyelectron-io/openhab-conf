from core.jsr223 import scope
from core.actions import NotificationAction, Mail
from configuration import admin_email, alert_email

log = logging.getLogger("{}.personal.utils".format(LOG_PREFIX))

def notification(prefix, message, priority=0, audio=True, kodi=True, android=True): # priority 1 is urgent
    log.info("Notification: {}: {}".format(prefix, message))
    current_mode = scope.items["Mode"].toString()
    if android:
        if priority > 0 or scope.items["Presence"] == scope.StringType("Away") or current_mode in ["Night", "Late"]:
            NotificationAction.sendBroadcastNotification(message)
        else:
            if scope.items["Lisa_Region"] != scope.StringType("Home"):
                NotificationAction.sendNotification(lisa_email, message)
            if scope.items["Scott_Region"] != scope.StringType("Home"):
                NotificationAction.sendNotification(scott_email, message)
    if audio:
        if priority > 0 or (scope.items["Disable_Audio_Notification"] == scope.OFF and scope.items["Presence"] == scope.StringType("Home") and (current_mode not in ["Night", "Late"] or (current_mode == "Night" and "Time: " in message))):
            scope.events.sendCommand("Audio_Notification", message)
    if kodi:
        scope.events.sendCommand("Kodi_Notification", message)