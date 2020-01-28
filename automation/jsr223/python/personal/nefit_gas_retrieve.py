'''
----------------------------------------------------------------------------------------------------
nefit_gas_retrieve.py - Retrieve yesterdays gas usage for Hot Water (HW) and Central Heating (CH).
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
Retrieve yesterdays gas usage for Hot Water (HW) and Central Heating (CH).
The Nefit CV returns the gas usage in kWh, not in m3 (as measured by the utility
company). So we must convert this to m3. The Nefit Easy app uses a conversion factor
of 0.12307692F (kWh * 0.12307692f = m3) for natural gas, which means a caloric value
of 29 MJ/m3 (for Dutch users, this value is rather low, and a value of 35.17 MJ/m3
is more accurate. More information can be found on the Gasunie website).
Format of the JSON messages received (32 entries per page):
 {"id":"/ecus/rrc/recordings/gasusage","type":"recordings","recordable":0,"writeable":0,
   "value":[
     {"d":"08-01-2019","hw":18.3,"ch":85.9,"T":73},
     {"d":"09-01-2019","hw":20.5,"ch":83.1,"T":53},
     {"d":"10-01-2019","hw":2.1,"ch":91.9,"T":37},
     {"d":"11-01-2019","hw":9.5,"ch":80.5,"T":70},
     {"d":"12-01-2019","hw":17.9,"ch":66,"T":68},
        ...
     {"d":"255-256-65535","hw":6553.5,"ch":6553.5,"T":-1}
   ]
 }
For conversion of kWh to m3 natutal gas:
 1 kWh equals 3.6 MJ
 1 m3 = 35.17 MJ/3.6 MJ = 9.7694 kWh
 1 kWh = 0.102365 m3
Since Nefit is a Dutch brand of the Robert Bosch Group, the conversion is hardcoded.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
from core.actions import Exec
import configuration
reload(configuration)
from configuration import LOG_PREFIX, NEFIT_BRIDGE_URL, INFLUXDB, INFLUXDB_URL, NEFIT_HW_SERIES, NEFIT_CH_SERIES
from org.joda.time import DateTime
import json     # pylint: disable=unused-import
import requests

log = logging.getLogger("{}.nefit_gas_history".format(LOG_PREFIX))

#===================================================================================================
@rule("NefitGasHistory", description="Retrieve yesterdays gas usage for Hot Water Central Heating", tags=["energy"])
@when("Time cron 0 5 0 * * ?")      # Shortly after midnight
@when("Item CV_Retry_GasUsage changed to OFF")      # Retry trigger switch (expire)
def nefit_retrieve_gas_history(event):
    httpHeader = {'Content-Type': 'application/json'}

    #--- Get the number of gas usage pages from Nefit server
    response = requests.get(NEFIT_BRIDGE_URL + "/ecus/rrc/recordings/gasusagePointer", headers=httpHeader)
    if response.status_code != 200:
        log.warn("NefitEasy - Invalid API status response [{}]".format(response))
        events.sendCommand("CV_Retry_GasUsage", "ON")   #Set retry switch
    else:
        log.debug("Received Pages JSON data [{}]".format(response.json()))
        entries = float(response.json()["value"])
        log.info("Number of entries is [{0:.0f}]".format(entries))
        page = (entries - 1) / 32
        log.info("Page # is [{0:.0f}]".format(page))

        # Get the last web page for yesterdays data
        response = requests.get(NEFIT_BRIDGE_URL + "/ecus/rrc/recordings/gasusage?page="+str(page), headers=httpHeader)
        if response.status_code != 200:
            log.warn("NefitEasy - Invalid API status response [{}]".format(response))
            events.sendCommand("CV_Retry_GasUsage", "ON")   #Set retry switch
        else:
            log.debug("Received Nefit Bridge update [{}]".format(response.json()))
            # Walk through JSON Array and find yesterday's entry.
            yesterday = DateTime.now().minusDays(1).toString("dd-MM-yyyy")
            for g in response.json()['value']:
                if g['d'] == yesterday:
                    hotWater = "{0:.3f}".format(float(g['hw']) * 0.102365)
                    centralHeating = "{0:.3f}".format(float(g['ch']) * 0.102365)
                    influxTimestamp = DateTime.now().withTimeAtStartOfDay().minusSeconds(1).millis
                    log.info("Yesterdays Hot Water [{}], Central Heating [{}]".format(hotWater, centralHeating))
                    cmd = "/bin/sh@@-c@@/usr/bin/curl -s -X POST "+INFLUXDB_URL+"write?db="+INFLUXDB+"\\&precision=ms --data-binary '"+NEFIT_HW_SERIES+" value="+hotWater+" "+str(influxTimestamp)+"'"
                    log.info("CMD1 [{}]".format(cmd))
                    response = Exec.executeCommandLine(cmd, 4000)
                    if response != "":
                        log.warn("Error writing "+NEFIT_HW_SERIES+" value to InfluxDB [{}]".format(response))
                    cmd = "/bin/sh@@-c@@/usr/bin/curl -s -X POST "+INFLUXDB_URL+"write?db="+INFLUXDB+"\\&precision=ms --data-binary '"+NEFIT_CH_SERIES+" value="+centralHeating+" "+str(influxTimestamp)+"'"
                    log.info("CMD2 [{}]".format(cmd))
                    Exec.executeCommandLine(cmd, 4000)
                    if response != "":
                        log.warn("Error writing "+NEFIT_HW_SERIES+" value to InfluxDB [{}]".format(response))
                    return

            log.warn("No historic gas usage entry found for [{}]".format(yesterday))
