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
import base64
from core.actions import Exec

#--- Define the group name for all snapshot image items
GRAFANA_GROUP = "gSnapshot"

#--- Define constants for building the Grafana URL.
GRAFANA_URL_BASE = "http://192.168.2.2:3000/d/io6U2XyWz/openhab?orgId=1"  #&tz=Europe%2FAmsterdam"
GRAFANA_URL_THEME_DARK = "dark"
GRAFANA_URL_THEME_LIGHT = "light"
# GRAFANA_URL_RANGE_TODAY = "from=now%2Fd"
GRAFANA_URL_RANGE24H = "from=now-24h&to=now"
GRAFANA_URL_RANGE7D = "from=now-7d&to=now"

log = logging.getLogger("{}.grafana".format(LOG_PREFIX))

grafImgDict = {
    1: {
        "item_description": "Outdoor Temp last 24H",
        "item_name": "imgTempOutdoor24h",
        "item_group": "gSnapshot",
        "grafana_panelid": 4,
        "ftp_channel": "grf_temp_outdoor24h",
        "grafana_range_from": "now%2Fd",
        "grafana_range_to": "",
        "grafana_theme": GRAFANA_URL_THEME_DARK,
        "image_refresh": 60,
        "refresh_timer": None
    },
    2: {
        "item_description": "Indoor Temp last 24H",
        "item_name": "imgTempIndoor24h",
        "item_group": "gSnapshot",
        "grafana_panelid": 2,
        "ftp_channel": "grf_temp_indoor24h",
        "grafana_range_from":"now%2Fd",
        "grafana_range_to": "",
        "grafana_theme": GRAFANA_URL_THEME_DARK,
        "image_refresh": 10,
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
# For testing purposes only: Use this to show items metadata
@log_traceback
def showGrafanaItems():
    showGrafanaItems.log = logging.getLogger("{}.showGrafanaItems".format(LOG_PREFIX))
    from core.metadata import get_metadata
    for item in itemRegistry.getAll():
        metadata = get_metadata(item.name, "Grafana_Graphs")
        if metadata is not None:
            showGrafanaItems.log.warn("{}\n{}".format(item, metadata.configuration))


#---------------------------------------------------------------------------------------------------
def addGrafanaItems():
    # create Grafana Items and groups, if they do not exist
    addGrafanaItems.log = logging.getLogger("{}.addGrafanaItems".format(LOG_PREFIX))

    scriptExtension.importPreset("RuleSupport")

    from core.utils import ChannelUID
    from core.items import add_item
    from core.links import add_link
    from core.metadata import set_metadata

    try:
        for entry in grafImgDict.values():
            imgItemName = entry.get("item_name")
            if ir.getItems(imgItemName) == []:
                addGrafanaItems.log.info("Adding item [{}]".format(imgItemName))
                add_item(imgItemName, item_type="Image", groups=[entry.get("item_group")], label=entry.get("item_description"), tags=["Grafana"])
                addGrafanaItems.log.info("Created item [{}]".format(imgItemName))
                grafanaChannel = ChannelUID("ftpupload:imagereceiver:"+entry.get("ftp_channel")+":image")
                add_link(imgItemName, grafanaChannel)
            else:
                addGrafanaItems.log.info("Item [{}] exists".format(imgItemName))
            set_metadata(imgItemName, "Grafana_Graphs", \
                {"PanelId": entry.get("grafana_panelid"), \
                "RefreshRate": entry.get("image_refresh"), \
                "RangeFrom": entry.get("grafana_range_from"), \
                "RangeTo": entry.get("grafana_range_to"), \
                "Theme": entry.get("grafana_theme")}, overwrite=True)
            addGrafanaItems.log.info("Item [{}] metadata set".format(imgItemName))
    except:
        import traceback
        addGrafanaItems.log.error(traceback.format_exc())


#---------------------------------------------------------------------------------------------------
def scriptLoaded(id):
    # removeGrafanaItems()    # For testing purposes only
    addGrafanaItems()
    showGrafanaItems()      # For testing purposes only


#---------------------------------------------------------------------------------------------------
# Function for retrieving the PNG snapshot file
def getSnapshotImage(url, img):
    getSnapshotImage.log = logging.getLogger("{}.grafanaRefreshInit".format(LOG_PREFIX))

    tmpFile = "/tmp/"+img+".png"
    Exec.executeCommandLine("wget -O " + tmpFile + " \"" + url + "\"", 10000)
    # getSnapshotImage.log.info(u"Exec result is [{}]".format(result))
    with open(tmpFile, "rb") as f:
        return "data:image/png;base64,"+base64.b64encode(f.read())


#===================================================================================================
@rule("GrafanaRefreshInit", description="Initialize Grafana snapshot refresh from Dictionary", tags=["graphs"])
@when("System started")
def grafanaRefreshInit(event):
    grafanaRefreshInit.log = logging.getLogger("{}.grafanaRefreshInit".format(LOG_PREFIX))

    from core.metadata import get_key_value

    grafanaRefreshInit.log.info("Enter GrafanaRefreshInit")

    for item in ir.getItem(GRAFANA_GROUP).members:
        grafanaRefreshInit.log.info("Iterate group [{}] - item [{}]".format(GRAFANA_GROUP, item.name))
        panelUrl = GRAFANA_URL_BASE+"&panelId="+str(get_key_value(item.name, "Grafana_Graphs", "PanelId")) + \
            "&from="+str(get_key_value(item.name, "Grafana_Graphs", "RangeFrom")) + \
            "&fullscreen&kiosk"
        rangeTo = str(get_key_value(item.name, "Grafana_Graphs", "RangeTo"))
        if rangeTo != "":
            panelUrl += "&to="+rangeTo
        grafanaRefreshInit.log.info("Item URL [{}]".format(panelUrl))
        imageSnapshot = getSnapshotImage(panelUrl, item.name)
        events.postUpdate(item.name, imageSnapshot)
