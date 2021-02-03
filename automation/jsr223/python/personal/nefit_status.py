'''
----------------------------------------------------------------------------------------------------
nefit_status.py - Get the Nefit CH/HW system status every minute (from the easy-server daemon).
----------------------------------------------------------------------------------------------------
Changelog:
20200130 v01    Created initial script.
----------------------------------------------------------------------------------------------------
See https://github.com/robertklep/nefit-easy-http-server.

The API command '/api/status' returns the following JSON result:
{    "user mode":"clock",
     "clock program":"auto",
     "in house status":"ok",
     "in house temp":21.2,
     "hot water active":false,
     "boiler indicator":"off",
     "control":"room",
     "temp override duration":0,
     "current switchpoint":8,
     "ps active":false,
     "powersave mode":false,
     "fp active":false,
     "fireplace mode":false,
     "temp override":true,
     "holiday mode":false,
     "boiler block":null,
     "boiler lock":null,
     "boiler maintenance":null,
     "temp setpoint":20.5,
     "temp override temp setpoint":20.5,
     "temp manual setpoint":20,
     "hed enabled":null,
     "hed device at home":null,
     "outdoor temp":3,
     "outdoor source type":"virtual"
}
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX, NEFIT_API_URL, NEFIT_BRIDGE_URL
import json # pylint: disable=unused-import
import requests
from core.utils import sendCommandCheckFirst
from core.actions import PersistenceExtensions


#==================================================================================================
@rule("Nefit Easy Status Update", description="Get the Nefit CH/HW system status every minute", tags=["energy"])
@when("Time cron 0 * * * * ?")
def nefitStatus(event):
    httpHeader = {'Content-Type': 'application/json'} #,'Cache-Control': 'no-cache','Pragma': 'no-cache'}
    #--- Get Nefit thermostat info from the easy-server API
    response = requests.get(NEFIT_API_URL+"/status", headers=httpHeader)
    if response.status_code != 200:
        nefitStatus.log.warn("NefitEasy - Invalid API status response [{}]".format(response))
    else:
        #-- Get the relevant parameters ('in house temp' and 'temp setpoint') from the JSON response.
        try:
            events.postUpdate("CV_Temp_Livingroom", "{0:.1f}".format(response.json()["in house temp"]))
        except:
            nefitStatus.log.warn("Error setting in house temp; JSON response [{}]".format(response.json()))
        try:
            events.postUpdate("CV_SetPoint_Livingroom", "{0:.1f}".format(response.json()["temp setpoint"]))
        except:
            nefitStatus.log.warn("Error setting setpoint temp; JSON response [{}]".format(response.json()))
    #--- Get Nefit Heater water pressure
    response = requests.get(NEFIT_BRIDGE_URL+"/system/appliance/systemPressure", headers=httpHeader)
    if response.status_code != 200:
        nefitStatus.log.warn("NefitEasy - Invalid API pressure response [{}]".format(response))
    else:
        try:
            events.postUpdate("CV_Pressure", "{0:.1f}".format(response.json()['value']))
            events.sendCommand("CV_Watchdog", "ON")
        except:
            nefitStatus.log.warn("Error setting Nefit water pressure; JSON response [{}]".format(response.json()))
    #--- Get Nefit CV burner data
    response = requests.get(NEFIT_BRIDGE_URL+"/ecus/rrc/uiStatus", headers=httpHeader)
    if response.status_code != 200:
        nefitStatus.log.warn("NefitEasy - Invalid API burner status response [{}]".format(response))
    else:
        # Extract the relevant info from the JSON data
        try:
            burner = response.json()['value']['BAI']
        except:
            nefitStatus.log.warn("Error reading Nefit burner status; JSON response [{}]".format(response.json()))
            burner = "No"
        if burner == "CH":
            sendCommandCheckFirst("CV_Heater_Active", "ON")
            sendCommandCheckFirst("CV_HotWater_Active", "OFF")
        elif burner == "HW":
            sendCommandCheckFirst("CV_Heater_Active", "OFF")
            sendCommandCheckFirst("CV_HotWater_Active", "ON")
        else:
            sendCommandCheckFirst("CV_Heater_Active", "OFF")
            sendCommandCheckFirst("CV_HotWater_Active", "OFF")


#===================================================================================================
@rule("Nefit Check Online", description="Check if Netfit and Netatmo devices are still sending updates", tags=["heating"])
@when("Item CV_Temp_Livingroom received update")
@when("Item NHC_Temp_Livingroom received update")
def nefitCheck(event):
    nefitCheck.log.debug("Received update from {}, reset watchdog".format(event.itemName))
    events.sendCommand("CV_Watchdog" if event.itemName == "CV_Temp_Livingroom" else "NHC_Watchdog", "ON")


#===================================================================================================
@rule("Nefit Control Floor Pump", description="Switch Floor heating Pump based on CV status", tags=["heating"])
@when("Item CV_Heater_Active received command")
def nefitPumpCheck(event):
    nefitPumpCheck.log.info("{name} received command {command}".format(name=event.itemName, command=event.itemCommand))
    if str(event.itemCommand) == "OFF":
        nefitPumpCheck.log.info("CV heater switched off, wait 5 minutes before turning off the Floor Pump")
        if str(ir.getItem("Shelly_FloorPump_Switch")) == "OFF":
            nefitPumpCheck.log.info("Shelly FloorPump is already off, exit rule")
            return
        nefitPumpCheck.log.info("Shelly Floor Pump is on, set 5 minute expire switch")
        events.sendCommand("CV_Pump_Off", "ON")
    if str(event.itemCommand) == "ON":
        nefitPumpCheck.log.info("CV heater switched on, turn on the Floor Pump")
        events.sendCommand("CV_Pump_Off", "OFF")
        events.sendCommand("Shelly_FloorPump_Switch", "ON")


#===================================================================================================
@rule("CV Floor Pump", description="Switch Floor heating Pump based on CV status", tags=["heating"])
@when("Item CV_Pump_Off received command")
def nefitPumpSwitch(event):
    nefitPumpSwitch.log.info("{name} received command {command}".format(name=event.itemName, command=event.itemCommand))
    if str(event.itemCommand) == "OFF":
        nefitPumpSwitch.log.info("CV Pump off timer expired")
        if str(ir.getItem("CV_Heater_Active").state) == "ON":
            # events.sendCommand("CV_Pump_Off", "ON")
            nefitPumpSwitch.log.info("Timer expired but CV heater is active again, ignore timer")
        else:
            events.sendCommand("Shelly_FloorPump_Switch", "OFF")
            nefitPumpSwitch.log.info("Timer expired, turn off the CV floor pump")

#===================================================================================================
#@rule("NefitNextProgram", description="Get the next programmed switch point (from the easy-server daemon)", tags=["heating"])
#@when("Time cron */10 * * * * ?)
#def nefit_get_next_program(event):
'''
 See https://github.com/robertklep/nefit-easy-http-server.

 The API command '/api/program' returns the following JSON result:
    {   "active":1,
        "program1":
        [   {"dow":0,"time":"07:15","temp":19.5},
            {"dow":0,"time":"08:30","temp":20},
            {"dow":0,"time":"11:30","temp":21},
            {"dow":0,"time":"22:50","temp":19.5},
            {"dow":1,"time":"06:15","temp":20},
              ...
            {"dow":6,"time":"23:50","temp":19.5}
        ],
        "program2":
        [   {"dow":0,"time":"07:00","temp":20},
	     	{"dow":0,"time":"23:00","temp":20},
	  	    {"dow":1,"time":"07:00","temp":20},
	  	    {"dow":1,"time":"23:00","temp":20},
              ...
        ]
    Day of week 0 is Sunday.
'''
    # # Get Nefit Easy program info in JSON format from the easy-server API.
    # response = requests.get(NEFIT_API_URL+"/program", headers=httpHeader)
    # if response.status_code != 200:
    #     log.warn("NefitEasy - Invalid API status response [{}]".format(response))
    # else:
    #     # Get the active program.
    #     try:
    #         activeProgram = response.json()["active"]
    #     except:
    #         log.warn("Error getting active program; JSON input was[{}]".format(response.json()))
    #     # Get the current time and day of week (0 = Sunday).
    #     # ...

#===================================================================================================
# @rule("NefetSetpointChange", description="Change the thermostat SetPoint and disable program mode", taggs=["heating"])
# @when("Item CV_Temp_Livingroom received command")
# def nefit_setpoint_change(event):
#     httpHeader = "application/json"
#     if items.CV_Temp_Livingroom is not None:
#         response = requests.post(NEFIT_BRIDGE_URL+"/heatingCircuits/hc1/temperatureRoomManual", headers=httpHeader, '{"value":' + items.CV_Temp_Livingroom + '}')
#         log.info("Nefit Setpoint 1 [{}]".format(response.text))
#         endpoint2 = "/heatingCircuits/hc1/manualTempOverride/status"
#         output = sendHttpPostRequest(NEFIT_BRIDGE_URL+endpoint2, contenttype, '{ "value":"on" }')
#         log.info("Nefit Setpoint 2 [{}]".format(output))

#         endpoint3 = "/heatingCircuits/hc1/manualTempOverride/temperature"
#         output = sendHttpPostRequest(NEFIT_BRIDGE + endpoint3, contenttype, POSTrequest)
#         log.info("Nefit Setpoint 3 [{}]".format(output))
#     else:
#         log.warn("[{}] is NULL, skipping rule".format(event.itemName))

# // // Check if the livingroom or dining door is open and lower the thermostat while
# // // either is open.
# // rule "Heating off when livingroom or kitchen door open"
# // 	when
# //         Item Alarm_Door_Livingroom changed to OPEN or
# //         Item Alarm_Door_Dining changed to OPEN
# // 	then
# //         // Save the current setpoint if this is the first door open event
# //         if (nSavedSetpoint == 0)
# //         {
# //             logInfo(TAG, "Saving current setPoint {}", CV_Temp_Livingroom.state)
# //             nSavedSetpoint = CV_Temp_Livingroom.state as Number
# //         }

# //         // Lower the setpoint to 18 while at least one of the doors is open
# //         logInfo(TAG, "Door is open. Temporary lower the setpoint to 18 degrees celcius")
# //         CV_Temp_Livingroom.sendCommand(18)


# // // Check if both the livingroom or dining door are closed and restore the thermostat
# // // setpoint if both are closed.
# // rule "Restore setpoint when doors are closed"
# //     when
# //         Item Alarm_Door_Livingroom changed to CLOSED or
# //         Item Alarm_Door_Dining changed to CLOSED
# // 	then
# //         val String TAG = "NefitEasy."+triggeringItem.name+".DoorClose"

# //         // Check if both doors are closed now
# //         if (Alarm_Door_Livingroom.state == CLOSED && Alarm_Door_Dining.state == CLOSED)
# //         {
# //             if (nSavedSetpoint > 0)
# //             {
# //                 logInfo(TAG, "Restoring setpoint to {}, both doors are now closed", nSavedSetpoint)
# //                 CV_Temp_Livingroom.sendCommand(nSavedSetpoint)
# //             }
# //             nSavedSetpoint = 0
# //         }
# //         else
# //             logInfo(TAG, "Skip restore of heater SetPoint, not all doors are closed")


# // // Check if the livingroom or dining door is open and lower the thermostat while
# // // either is open.
# // rule "Nefit.Presence.Change - Heating adjustment based on presence"
# // 	when
# //         Item Presence_Ron changed or
# //         Item Presence_Arniel changed
# // 	then
# //         val String TAG = "Nefit."+triggeringItem.name+".Change"
# //         logInfo(TAG, ">>>>>> Enter rule - with trigger {}, prev {}", triggeringItem, previousState.toString)
# //         if (previousState == NULL)
# //             return;

# //         if ((Presence_Ron.state != NULL && Presence_Ron.state == ON) || (Presence_Arniel.state != NULL && Presence_Arniel.state == ON))
# //         {
# //             // Someone is home, increase setpoint based on TOD
# //             logInfo(TAG, "We're home, do something usefull with that information...")
# //         }
