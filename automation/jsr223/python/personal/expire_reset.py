from core.rules import rule
from core.triggers import when

@rule("Reset Expire Binding Timers", description="Sends an ON command to all members of gResetExpire if they were restoreOnStartup to ON", tags=["admin"])
@when("System started")
def reset_expire(event):
    reset_expire.log.info("Restarting Expire binding Timers")
    for timer in ir.getItem("gResetExpire").members:
        events.sendCommand(timer, ON)
