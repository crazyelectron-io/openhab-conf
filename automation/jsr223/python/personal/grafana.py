'''
----------------------------------------------------------------------------------------------------
grafana.py - handle Grafana snapshot generation+download for external use via the cloud server.
----------------------------------------------------------------------------------------------------
TODO: Generte channels and item definitions for images
Changelog:
20200202 v02    Fixed URL for direct rendered images. Added 2nd graph.
20200120 v01    Created initial (non-working) script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, log_traceback
import configuration
reload(configuration)
from configuration import LOG_PREFIX
import base64
from core.actions import Exec
from core.metadata import set_metadata, get_key_value

# Group name for all snapshot image items
GRAFANA_GROUP = "gSnapshot"

# Constants for building the Grafana URL
GRAFANA_URL_BASE = "http://192.168.2.2:3000/render/d-solo/io6U2XyWz/openhab?orgId=1&width=1000&height=500&tz=Europe%2FAmsterdam&fullscreen&kiosk"
GRAFANA_THEME_DARK = "dark"
GRAFANA_THEME_LIGHT = "light"

log = logging.getLogger("{}.grafana".format(LOG_PREFIX))

grafImgDict = {
    1: {
        "item_description": "Outdoor Temp last 24h",
        "item_name": "imgTempOutdoor24h",
        "item_group": "gSnapshot",
        "grafana_panelid": 4,
        "ftp_channel": "grf_temp_outdoor24h",
        "grafana_range_from": "now%2Dd",
        "grafana_range_to": "now",
        "grafana_theme": GRAFANA_THEME_DARK,
        "image_refresh": 15,
        "refresh_timer": None
    },
    2: {
        "item_description": "Indoor Temp last 24h",
        "item_name": "imgTempIndoor24h",
        "item_group": "gSnapshot",
        "grafana_panelid": 2,
        "ftp_channel": "grf_temp_indoor24h",
        "grafana_range_from":"now%2Dd",
        "grafana_range_to": "now",
        "grafana_theme": GRAFANA_THEME_DARK,
        "image_refresh": 15,
        "refresh_timer": None
    },
    3: {
        "item_description": "Power Consumption last 24h",
        "item_name": "imgPowerDelta24h",
        "item_group": "gSnapshot",
        "grafana_panelid": 6,
        "ftp_channel": "grf_pwr_delta24h",
        "grafana_range_from":"now%2Dd",
        "grafana_range_to": "now",
        "grafana_theme": GRAFANA_THEME_DARK,
        "image_refresh": 30,
        "refresh_timer": None
    },
}


#---------------------------------------------------------------------------------------------------
# For testing purposes only: Use this to remove created items
@log_traceback
def removeGrafanaItems():
    removeGrafanaItems.log = logging.getLogger("{}.removeGrafanaItems".format(LOG_PREFIX))
    from core.items import remove_item
    for item in ir.getItemsByTag("Grafana"):
        removeGrafanaItems.log.info("removeGrafanaItems: [{}]".format(item))
        remove_item(item)


#---------------------------------------------------------------------------------------------------
# *For Testing Purposes Only* - Use this to show items metadata
@log_traceback
def showGrafanaItems():
    showGrafanaItems.log = logging.getLogger("{}.showGrafanaItems".format(LOG_PREFIX))
    from core.metadata import get_metadata
    for item in itemRegistry.getAll():
        metadata = get_metadata(item.name, "Grafana_Graphs")
        if metadata is not None:
            showGrafanaItems.log.warn("{}\n{}".format(item, metadata.configuration))


#---------------------------------------------------------------------------------------------------
# Create Grafana Items and Groups, if they do not exist yet
def addGrafanaItems():
    addGrafanaItems.log = logging.getLogger("{}.addGrafanaItems".format(LOG_PREFIX))

    scriptExtension.importPreset("RuleSupport")

    from core.utils import ChannelUID
    from core.items import add_item
    from core.links import add_link

    try:
        for entry in grafImgDict.values():
            imgItemName = entry.get("item_name")
            addGrafanaItems.log.info("Item to process [{}]".format(imgItemName))
            if ir.getItems(imgItemName) == []:
                addGrafanaItems.log.info("Adding item [{}]".format(imgItemName))
                add_item(imgItemName, item_type="Image", groups=[entry.get("item_group")], label=entry.get("item_description"), tags=["Grafana"])
                addGrafanaItems.log.info("Created item [{}]".format(imgItemName))
                grafanaChannel = ChannelUID("ftpupload:imagereceiver:"+entry.get("ftp_channel")+":image")
                add_link(imgItemName, grafanaChannel)
            else:
                addGrafanaItems.log.info("Item [{}] exists".format(imgItemName))
            addGrafanaItems.log.info("Add metadate to [{}]".format(imgItemName))
            set_metadata(imgItemName, "Grafana_Graphs", \
                {"PanelId": entry.get("grafana_panelid"), \
                "RefreshRate": entry.get("image_refresh"), \
                "RangeFrom": entry.get("grafana_range_from"), \
                "RangeTo": entry.get("grafana_range_to"), \
                "Theme": entry.get("grafana_theme"), \
                "RefreshTimer": entry.get("refresh_timer")}, overwrite=True)
            addGrafanaItems.log.info("Metadata set [{}] [{}] [{}] [{}]".format(get_key_value(imgItemName, "Grafana_Graphs", "PanelId"), get_key_value(imgItemName, "Grafana_Graphs", "RefreshRate"), get_key_value(imgItemName, "Grafana_Graphs", "Theme"), get_key_value(imgItemName, "Grafana_Graphs", "RefreshTImer")))
    except:
        import traceback
        addGrafanaItems.log.error(traceback.format_exc())


#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    removeGrafanaItems()        # *For testing purposes only*
    addGrafanaItems()
    showGrafanaItems()          # *For testing purposes only*


#---------------------------------------------------------------------------------------------------
# Function for retrieving the PNG snapshot file
def getSnapshotImage(url, img):
    getSnapshotImage.log = logging.getLogger("{}.grafanaRefreshInit".format(LOG_PREFIX))

    tmpFile = "/tmp/"+img+".png"
    cmd = "wget -O " + tmpFile + " \"" + url + "\""
    getSnapshotImage.log.info("Commandline to retrieve image: [{}]".format(cmd))
    Exec.executeCommandLine(cmd, 10000)
    with open(tmpFile, "rb") as f:
        return "data:image/png;base64,"+base64.b64encode(f.read())


#---------------------------------------------------------------------------------------------------
# Function for refreshing the graph item
def refreshImageItem(itemName):
    getSnapshotImage.log = logging.getLogger("{}.grafanaRefreshInit".format(LOG_PREFIX))

    panelUrl = GRAFANA_URL_BASE+"&panelId=" + str(get_key_value(itemName, "Grafana_Graphs", "PanelId")) + \
        "&from=" + str(get_key_value(itemName, "Grafana_Graphs", "RangeFrom"))
    rangeTo = str(get_key_value(itemName, "Grafana_Graphs", "RangeTo"))
    if rangeTo != "":
        panelUrl += "&to="+rangeTo
    grafanaRefreshInit.log.info("Item URL [{}]".format(panelUrl))
    imageSnapshot = getSnapshotImage(panelUrl, itemName)
    events.postUpdate(itemName, imageSnapshot)


#===================================================================================================
@rule("GrafanaRefreshInit", description="Initialize Grafana snapshot refresh from Dictionary", tags=["graphs"])
@when("System started")
def grafanaRefreshInit(event):
    grafanaRefreshInit.log = logging.getLogger("{}.grafanaRefreshInit".format(LOG_PREFIX))

    grafanaRefreshInit.log.info("Grafana Refresh Init")

    for item in ir.getItem(GRAFANA_GROUP).members:
        grafanaRefreshInit.log.info("Iterate group [{}] - item [{}]".format(GRAFANA_GROUP, item.name))
        refreshImageItem(item.name)
        # Set timer for next refresh
        refreshTimer = get_key_value(item.name, "Grafana_Graphs", "RefreshTimer")
        imageRefresh = str(get_key_value(item.name, "Grafana_Graphs", "RefreshRate"))
        grafanaRefreshInit.log.info("Metadata - Refresh [{}], Timer [{}] (type [{}])".format(imageRefresh, refreshTimer, type(refreshTimer)))

        if refreshTimer is None or refreshTimer == {}:
            grafanaRefreshInit.log.info("Timer is None, start refresh time [{}] for [{}]".format(imageRefresh, item.name))

            # Do something
        else:
            grafanaRefreshInit.log.info("Timer is active, restart refresh time [{}] for [{}]".format(imageRefresh, item.name))

            # Do something else

