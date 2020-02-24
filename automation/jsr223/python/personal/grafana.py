'''
----------------------------------------------------------------------------------------------------
grafana.py - handle Grafana snapshot generation+download for external use via the cloud server.
----------------------------------------------------------------------------------------------------
TODO: Generate channels and item definitions for images
Changelog:
20200207 v04    Removed log declaration in rule (already handled in rule decorator).
20200205 v03    Removed extra logging, added creation of Grafana group.
20200203 v02    Fixed URL for direct rendered images. Added 2 more graphs.
20200120 v01    Created initial (non-working) script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.items import add_item,remove_item
from core.log import logging, log_traceback
from core.actions import Exec
from core.metadata import set_metadata, get_key_value
from core.utils import ChannelUID
from core.links import add_link
from core.date import minutes_between
from org.joda.time import DateTime
import base64
import configuration
reload(configuration)
from configuration import LOG_PREFIX, GRAFANA_URL_BASE

# Group name for all snapshot image items
GRAFANA_GROUP = "gSnapshot"

# Constants for building the Grafana URL
GRAFANA_URL = GRAFANA_URL_BASE + "/render/d-solo/io6U2XyWz/openhab?orgId=1&width=1000&height=500&tz=Europe%2FAmsterdam&fullscreen&kiosk"
GRAFANA_THEME_DARK = "dark"
GRAFANA_THEME_LIGHT = "light"

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
        "image_refresh": 5,
        "last_refresh": DateTime.now()
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
        "image_refresh": 5,
        "last_refresh": DateTime.now()
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
        "image_refresh": 10,
        "last_refresh": DateTime.now()
    },
}

#---------------------------------------------------------------------------------------------------
# For testing purposes only: Use this to remove created items
@log_traceback
def removeGrafanaItems():
    removeGrafanaItems.log = logging.getLogger("{}.removeGrafanaItems".format(LOG_PREFIX))
    removeGrafanaItems.log.info("Remove existing Items...")
    for item in ir.getItemsByTag("Grafana"):
        removeGrafanaItems.log.info("Remove Grafana Item [{}]".format(item.name))
        remove_item(item)
    remove_item(GRAFANA_GROUP)

#---------------------------------------------------------------------------------------------------
# *For Testing Purposes Only* - Use this to show created items metadata
@log_traceback
def showGrafanaItems():
    showGrafanaItems.log = logging.getLogger("{}.showGrafanaItems".format(LOG_PREFIX))
    removeGrafanaItems.log.info("Show Items metadata...")
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
    # Add Grafana Group if it doesn't exist
    if ir.getItems(GRAFANA_GROUP) == []:
        addGrafanaItems.log.info("Create Group [{}]".format(GRAFANA_GROUP))
        add_item(GRAFANA_GROUP, item_type="Group", label="Grafana Snapshot images", tags=["Grafana"])
    else:
        addGrafanaItems.log.info("Group [{}] already exists".format(GRAFANA_GROUP))
    try:
        for entry in grafImgDict.values():
            imgItemName = entry.get("item_name")
            if ir.getItems(imgItemName) == []:
                add_item(imgItemName, item_type="Image", groups=[entry.get("item_group")], label=entry.get("item_description"), tags=["Grafana"])
                grafanaChannel = "ftpupload:imagereceiver:"+entry.get("ftp_channel")+":image"
                addGrafanaItems.log.info("Created item [{}], link channel [{}]".format(imgItemName, grafanaChannel))
                add_link(imgItemName, ChannelUID(grafanaChannel))
            set_metadata(imgItemName, "Grafana_Graphs", \
                {"PanelId": entry.get("grafana_panelid"), \
                "RefreshRate": entry.get("image_refresh"), \
                "RangeFrom": entry.get("grafana_range_from"), \
                "RangeTo": entry.get("grafana_range_to"), \
                "Theme": entry.get("grafana_theme"), \
                "LastRefresh": entry.get("last_refresh")}, overwrite=True)
            addGrafanaItems.log.info("Metadata set [{}] [{}] [{}] [{}]".format(get_key_value(imgItemName, "Grafana_Graphs", "PanelId"), get_key_value(imgItemName, "Grafana_Graphs", "RefreshRate"), get_key_value(imgItemName, "Grafana_Graphs", "Theme"), get_key_value(imgItemName, "Grafana_Graphs", "LastRefresh")))
    except:
        import traceback
        addGrafanaItems.log.error(traceback.format_exc())

#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    # removeGrafanaItems()        # *For testing purposes only*
    addGrafanaItems()
    # showGrafanaItems()          # *For testing purposes only*

#---------------------------------------------------------------------------------------------------
# Retrieve the PNG snapshot file.
def getSnapshotImage(url, img):
    tmpFile = "/tmp/"+img+".png"
    Exec.executeCommandLine("wget -O " + tmpFile + " \"" + url + "\"", 12000)
    with open(tmpFile, "rb") as f:
        return "data:image/png;base64,"+base64.b64encode(f.read())

#---------------------------------------------------------------------------------------------------
# Refresh the image Item.
def refreshImageItem(itemName):
    refreshImageItem.log = logging.getLogger("{}.grafanaRefreshInit".format(LOG_PREFIX))
    panelUrl = GRAFANA_URL + "&panelId=" + \
            str(get_key_value(itemName, "Grafana_Graphs", "PanelId")) + \
            "&from=" + str(get_key_value(itemName, "Grafana_Graphs", "RangeFrom"))
    rangeTo = str(get_key_value(itemName, "Grafana_Graphs", "RangeTo"))
    if rangeTo != "":
        panelUrl += "&to="+rangeTo
    refreshImageItem.log.debug("Refresh Item URL [{}]".format(panelUrl))
    imageSnapshot = getSnapshotImage(panelUrl, itemName)
    events.postUpdate(itemName, imageSnapshot)

#===================================================================================================
@rule("Grafana Snapshots Refresh", description="Grafana snapshots rendering refresh", tags=["graphs"])
@when("System started")
@when("Time cron 0 */3 * * * ?")
def grafanaRefresh(event):
    if ir.getItems(GRAFANA_GROUP) == []:
        addGrafanaItems() # Just in case
    for item in ir.getItem(GRAFANA_GROUP).members:
        lastRefresh = get_key_value(item.name, "Grafana_Graphs", "LastRefresh")
        grafanaRefresh.log.debug("Last refresh time for [{}] was [{}]".format(item.name, lastRefresh))
        if minutes_between(lastRefresh, DateTime.now()) >= get_key_value(item.name, "Grafana_Graphs", "RefreshRate"):
            refreshImageItem(item.name)
            set_metadata(item.name, "Grafana_Graphs", {"LastRefresh": DateTime.now()})
            grafanaRefresh.log.debug("New refresh time for [{}] set to [{}]".format(item.name, get_key_value(item.name, "Grafana_Graphs", "LastRefresh")))
