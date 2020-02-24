'''
----------------------------------------------------------------------------------------------------
volvo_heater.py - Turn the preclimatization on or off
----------------------------------------------------------------------------------------------------
Changelog:
20200207 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.jsr223.scope import actions

#===================================================================================================
@rule("Switch Preclimatization", description="Turn the Volvo preclimatization on or off", tags=["car"])
@when("Item VoC_Heater changed")
def volvoHeater(event):
    action = actions.get("volvooncall","volvooncall:vehicle:v90:V90")
    if action is None:
        volvoHeater.log.info("Actions not found (check thing ID)")
        return
    volvoHeater.log.info("Calling preclimatization action with [{}] status".format(event.itemState))
    if event.itemState == ON:
        action.preclimatizationStartCommand()
    elif event.itemState == OFF:
        action.preclimatizationStopCommand()
    else:
        volvoHeater.log.warn("Inavlid state for VoC preclimatization action")