'''
----------------------------------------------------------------------------------------------------
energy_gas.py - handle the data from the Smart Meter and Solar Panels.
----------------------------------------------------------------------------------------------------
Changelog:
20200116 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX, GAS_PRICE_PER_DM3
from core.actions import PersistenceExtensions
from org.joda.time import DateTime


log = logging.getLogger("{}.gas_use".format(LOG_PREFIX))
contractStart = DateTime.now().withTimeAtStartOfDay().withDayOfYear(15)  #Contract started at January 15.


#==================================================================================================
@rule("Calculate Gas Usage", description="Calculate the periodic gas usage and cost", tags=["energy"])
@when("Item Gas_Use_Total changed")
def gasUsage(event):
    global contractStart

    if event.oldItemState is None:
        return

    gasUsage.log = logging.getLogger("{}.gasUsage".format(LOG_PREFIX))

    # Calculate consumption last hour
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem("Gas_Use_Total"), DateTime.now().minusHours(1))))
    gasUsage.log.info("Last Hours Gas Usage [{0:.3f}]".format(used/1000))
    events.postUpdate("Gas_Use_Hour", "{0:.3f}".format(used))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Hour_Cost", "{0:.2f}".format(cost))
    events.postUpdate("Gas_Use_Hour_Summary", "{0:.3f} m3, EUR {1:.2f}".format(used/1000, cost))

    # # Calculate consumption today
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem("Gas_Use_Total"), DateTime.now().withTimeAtStartOfDay())))
    gasUsage.log.info("Today's Gas Ussage [{0:.3f}]".format(used/1000))
    events.postUpdate("Gas_Use_Day", "{0:.3f}".format(used))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Day_Cost", "{0:.2f}".format(cost))
    events.postUpdate("Gas_Use_Day_Summary", "{0:.3f} m3, EUR {1:.2f}".format(used/1000, cost))

    # # Calculate consumption this month
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem("Gas_Use_Total"), DateTime.now().withTimeAtStartOfDay().withDayOfMonth(1))))
    gasUsage.log.info("This Month's Gas Usage [{0:.3f}]".format(used/1000))
    events.postUpdate("Gas_Use_Month", "{0:.3f}".format(used))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Month_Cost", "{0:.2f}".format(cost))
    events.postUpdate("Gas_Use_Month_Summary", "{0:.3f} m3, EUR {1:.2f}".format(used/1000, cost))

    # # Calculate consumption this year
    # used = Gas_Use_Total.deltaSince(contractStart, "influxdb")
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem("Gas_Use_Total"), contractStart)))
    if used is None:
        used = float(str(items["Gas_Use_Total"])) - 7374000
        gasUsage.log.info("Fix for missing year data, pre-fill [{}]".format(used))

    gasUsage.log.info("This Contract Year's Gas Usage [{0:.3f}]".format(used/1000))
    # events.postUpdate("Gas_Use_Year", str(used))
    cost = used * GAS_PRICE_PER_DM3
    # events.postUpdate("Gas_Use_Year_Cost", str(cost))
    events.postUpdate("Gas_Use_Year_Summary", "{0:.3f} m3, EUR {1:.2f}".format(used/1000, cost))
