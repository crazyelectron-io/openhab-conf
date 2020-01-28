'''
----------------------------------------------------------------------------------------------------
grafana.py - handle Grafana snapshot generation+download for external use via the cloud server.
----------------------------------------------------------------------------------------------------
Changelog:
20200120 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX,DAY_PHASES_DICT
from org.joda.time import DateTime
from core.utils import postUpdateCheckFirst #,postUpdateIfDifferent
# import java.nio.file.FileSystems;
# import java.nio.file.Files;

#--- Define constants for building the Grafana URL.
GRAFANA_URL_BASE = "http://192.168.2.2:3000/render/d-solo/DRmxtepWz/openhab2?orgId=1"  #&tz=Europe%2FAmsterdam"
GRAFANA_URL_RANGE24H = "&from=now-24h&to=now"
GRAFANA_URL_RANGE7D = "&from=now-7d&to=now"
GRAFANA_URL_RANGE_TODAY = "&from=now%2Fd"
GRAFANA_URL_THEME_DARK = "&theme=dark"
GRAFANA_URL_THEME_LIGHT = "&theme=light"

log = logging.getLogger("{}.grafana".format(LOG_PREFIX))

grafImgDict = {
    "T1": {
        "use_price": 0.00022609,
        "return_price": 0.00022609,
        "use_more": 0.00007000,
        "return_more": 0.00007000
    },
    "T2": {
        "use_price": 0.00023819,
        "return_price": 0.00023819,
        "use_more": 0.00007000,
        "return_more": 0.00007000
    }
}


#---------------------------------------------------------------------------------------------------
# def get_snapshot_image(url, img):
#     # Function for retreiving the PNG snapshot file
#     tmpFile = "/tmp/"+img+".png"
#     result = executeCommandLine("wget -O " + tmpFile + " \"" + url + "\"", 10000)
#  	log.info("Retreive snapshot into [{}], result is [{}]".format(tmpFile, result))
#     fileData = Files.readAllBytes(FileSystems.getDefault().getPath(tmpFile))
#  	return "data:image/png;base64,"+java.util.Base64.encoder.encodeToString(fileData)

#===================================================================================================
@rule("GrafanaRefresh60", description="Refresh Grafana snapshot images every hour", tags=["graphs"])
@when("Time cron 0 0 * * * ? *")
@when("System started")
def grafana_refresh_60(event):
    GRAFANA_URL = GRAFANA_URL_BASE + GRAFANA_URL_RANGE24H + GRAFANA_URL_THEME_DARK
    log.info("Refresh Grafana snapshot from URL [{}]".format(GRAFANA_URL))
# 	gSnapshots60?.members.forEach[imgItem |
# 	    itemPanel = imgItem.name.substring(imgItem.name.lastIndexOf('_')+1, imgItem.name.length())
# 		imageSnapshot = get_snapshot_image.apply(GRAFANA_URL+"&panelId="+itemPanel, imgItem.name)
# 		log.info("60min update [{}] with Grafana base64 image snapshot".format(imgItem.name))
# 	    events.postUpdate(imgItem.name, imageSnapshot)

#===================================================================================================
@rule("GrafanaRefresh15", description="Refresh Grafana snapshot images every 15 minutes", tags=["graphs"])
@when("Time cron 0 */15 * * * ? *")
@when("System started")
def grafana_refresh_15(event):
    GRAFANA_URL = GRAFANA_URL_BASE + GRAFANA_URL_RANGE_TODAY + GRAFANA_URL_THEME_LIGHT
    log.info("Refresh Grafana snapshot from URL [{}]".format(GRAFANA_URL))
#	gSnapshots15?.members.forEach[imgItem |
#       itemPanel = imgItem.name.substring(imgItem.name.lastIndexOf('_')+1, imgItem.name.length())
# 		imageSnapshot = get_snapshot_image.apply(GRAFANA_URL+"&panelId="+itemPanel, imgItem.name)
# 		log.info("15min update [{}] with Grafana base64 image snapshot".format(imgItem.name))
# 	    events.postUpdate(imgItem.name, imageSnapshot)

#===================================================================================================
@rule("GrafanaRefresh10", description="Refresh Grafana snapshot images every 10 minutes", tags=["graphs"])
@when("Time cron 0 */10 * * * ? *")
@when("System started")
def grafana_refresh_10(event):
    GRAFANA_URL = GRAFANA_URL_BASE + GRAFANA_URL_RANGE_TODAY + GRAFANA_URL_THEME_DARK
    log.info("Refresh Grafana snapshot from URL [{}]".format(GRAFANA_URL))
# 	gSnapshots10?.members.forEach[imgItem |
#       itemPanel = imgItem.name.substring(imgItem.name.lastIndexOf('_')+1, imgItem.name.length())
#   	imageSnapshot = get_snapshot_image.apply(GRAFANA_URL+"&panelId="+itemPanel, imgItem.name)
#   	logDebug(TAG, "10min update [{}] with Grafana base64 image snapshot".format(imgItem.name))
#       events.postUpdate(imgItem.name, imageSnapshot)
