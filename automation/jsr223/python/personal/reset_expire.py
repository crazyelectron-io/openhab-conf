'''
----------------------------------------------------------------------------------------------------
reset_expire.py - Reset the expire binding that are in group gResetExpire
----------------------------------------------------------------------------------------------------
20200120 v01  Initial version.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when

@rule("Reset Expire Binding Timers", description="Sends an update to all members of gResetExpire of their restored state", tags=["admin"])
@when("System started")
def resetExpire(event):
    resetExpire.log.info("Restarting Expire binding Timers")
    for timer in ir.getItem("gResetExpire").members:
        events.postUpdate(timer, timer.getState())

# // //--------------------------------------------------------------------------------------------------
# // // Triggered when watchdog timer expires indicating we didn't receive data for 30 minutes.
# // // Send a notification to the user via OH Cloud Notifications.
# // //--------------------------------------------------------------------------------------------------
# // rule "Watchdog timeout triggered"
# //     when
# // 	Item CV_Watchdog changed to OFF
# //     then
# //         val String msg = "Nefit readings missing, check the Easy-Server status"
# //         logWarn("Nefit.Watchdog.Timeout", msg)
# //         sendBroadcastNotification(msg)
# //     end
