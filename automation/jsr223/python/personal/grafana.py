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
from core.log import logging, log_traceback
import configuration
reload(configuration)
from configuration import LOG_PREFIX
# from org.joda.time import DateTime
# import java.nio.file.FileSystems;
# import java.nio.file.Files;
# from threading import Timer

#--- Define constants for building the Grafana URL.
GRAFANA_URL_BASE = "http://192.168.2.2:3000/render/d-solo/DRmxtepWz/openhab2?orgId=1"  #&tz=Europe%2FAmsterdam"
GRAFANA_URL_THEME_DARK = "&theme=dark"
GRAFANA_URL_THEME_LIGHT = "&theme=light"
GRAFANA_URL_RANGE_TODAY = "&from=now%2Fd"
GRAFANA_URL_RANGE24H = "&from=now-24h&to=now"
GRAFANA_URL_RANGE7D = "&from=now-7d&to=now"

log = logging.getLogger("{}.grafana".format(LOG_PREFIX))

grafImgDict = {
    1: {
        "item_description": "Outdoor Temp last 24H",
        "item_name": "testTempOutdoor24H",
        "item_group": "gSnapshot60",
        "grafana_panelid": 4,
        "ftp_channel": "grf_temp_outdoor24h",
        "grafana_range": GRAFANA_URL_RANGE_TODAY,
        "grafana_theme": GRAFANA_URL_THEME_DARK,
        "image_refresh": 60,
        "refresh_timer": None
    },
    2: {
        "item_description": "Indoor Temp last 24H",
        "item_name": "testTempIndoor24H",
        "item_group": "gSnapshot10",
        "grafana_panelid": 2,
        "ftp_channel": "grf_temp_indoor24h",
        "grafana_range": GRAFANA_URL_RANGE_TODAY,
        "grafana_theme": GRAFANA_URL_THEME_DARK,
        "image_refresh": 10,
        "refresh_timer": None
    },
}

#---------------------------------------------------------------------------------------------------
@log_traceback
def removeGrafanaItems():
    # Use this to remove created items for testing
    removeGrafanaItems.log = logging.getLogger("{}.removeGrafanaItems".format(LOG_PREFIX))
    from core.items import remove_item

    for item in ir.getItemsByTag("Grafana"):
        removeGrafanaItems.log.info("removeGrafanaItems: [{}]".format(item))
        remove_item(item)

#removeOWMItems()


#---------------------------------------------------------------------------------------------------
def addGrafanaItems():
    # create Grafana Items and groups, if they do not exist
    addGrafanaItems.log = logging.getLogger("{}.addGrafanaItems".format(LOG_PREFIX))

    scriptExtension.importPreset("RuleSupport")

    from core.items import add_item

    try:
        for entry in grafImgDict.values():
            imgItemName = entry.get("item_name")
            log.info("Checking and creating item [{}]".format(imgItemName))
            if ir.getItems(imgItemName) == []:
                add_item(imgItemName, item_type="String", groups=[entry.get("item_group")], label=entry.get("item_description"), tags=["Grafana"])
                # TODO: Add metadata
    except:
        import traceback
        addGrafanaItems.log.error(traceback.format_exc())


#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    addGrafanaItems()


#---------------------------------------------------------------------------------------------------
# def get_snapshot_image(entry):
#     # Function for retrieving the PNG snapshot file
#     tmpFile = "/tmp/"+img+".png"
#     result = Exec.executeCommandLine("wget -O " + tmpFile + " \"" + url + "\"", 10000)
#     log.info("Retreive snapshot into [{}], result is [{}]".format(tmpFile, result))
#     # fileData = Files.readAllBytes(FileSystems.getDefault().getPath(tmpFile))
#     # return "data:image/png;base64,"+java.util.Base64.encoder.encodeToString(fileData)


#===================================================================================================
@rule("GrafanaRefreshInit", description="Initialize Grafana snapshot refresh from Dictionary", tags=["graphs"])
@when("System started")
def grafana_refresh_init(event):
    #--- Create image items from the dictionary if they don't exist


        # currentTimer = entry.get("refresh_timer")
        # if currentTimer is None or str(currentTimer.getState()) == "TERMINATED":
        #     currentTimer = Timer(entry.get("refresh_time")*60, lambda: get_snapshot_image(entry))

#       gSnapshots60?.members.forEach[imgItem |
# 	      itemPanel = imgItem.name.substring(imgItem.name.lastIndexOf('_')+1, imgItem.name.length())
# 		  imageSnapshot = get_snapshot_image.apply(GRAFANA_URL+"&panelId="+itemPanel, imgItem.name)
# 	      events.postUpdate(imgItem.name, imageSnapshot)