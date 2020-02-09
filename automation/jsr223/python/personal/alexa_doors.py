'''
----------------------------------------------------------------------------------------------------
alexa_doors.py - .
----------------------------------------------------------------------------------------------------
Changelog:
20200128 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.triggers import when
from core.rules import rule

#---------------------------------------------------------------------------------------------------
def get_lock_states():
    return "all doors are closed" if items["gDoors"] == CLOSED \
        else "the following doors are not closed, \n{}".format("\n".join(map(lambda unlockedLock: unlockedLock.label, \
            filter(lambda lock: lock.state == OPEN, ir.getItem("gDoors").getAllMembers()))))

#===================================================================================================
@rule("Alert: Voice command alert")
@when("Member of gAlexa_LastVoiceCommand received update")
def lastVoiceCommandAlert(event):
    if "doors close" in event.itemState.toString():
        lastVoiceCommandAlert.log.info("Recognized 'are all the doors closed' command")
        events.sendCommand(event.itemName.replace("LastVoiceCommand", "TTS"), get_lock_states())
    # elif event.itemState.toString() == "is the alarm on":
        # last_voice_command_alert.log.info("Recognized 'is the alarm on' command")
        # do stuff here
    # elif event.itemState.toString() == "is the bedroom airco on":
        # last_voice_command_alert.log.info("Recognized 'is the bedroom airco on' command")
        # do stuff here too
