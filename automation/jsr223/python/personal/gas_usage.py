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
# from core.log import logging
import configuration
reload(configuration)
from configuration import GAS_PRICE_PER_DM3
from core.actions import PersistenceExtensions
from org.joda.time import DateTime

# log = logging.getLogger("{}.gas_use".format(LOG_PREFIX))
contractStart = DateTime.now().withTimeAtStartOfDay().withDayOfYear(15)  #Contract started at January 15.

#==================================================================================================
@rule("Calculate Gas Usage", description="Calculate the periodic gas usage and cost", tags=["energy"])
@when("Item Gas_Use_Total changed")
def gasUsage(event):
    global contractStart
    if event.oldItemState is None:
        return

    # Calculate consumption last hour
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem(event.itemName), DateTime.now().minusHours(1))))
    events.postUpdate("Gas_Use_Hour", "{0:.3f}".format(used))
    gasUsage.log.info("Last Hour Gas Usage [{0:.3f} m3]".format(used/1000))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Hour_Cost", "{0:.2f}".format(cost))
    summary = u"{0:.2f} m3, € {1:.2f}".format(used/1000, cost)
    events.postUpdate("Gas_Use_Hour_Summary", summary)
    gasUsage.log.info(u"Gas Use Hour Summary [{}]".format(summary))

    # Calculate consumption today
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem(event.itemName), DateTime.now().withTimeAtStartOfDay())))
    events.postUpdate("Gas_Use_Day", "{0:.3f}".format(used))
    gasUsage.log.info("Today's Gas Ussage [{0:.3f}]".format(used/1000))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Day_Cost", "{0:.2f}".format(cost))
    events.postUpdate("Gas_Use_Day_Summary", u"{0:.1f} m3, € {1:.2f}".format(used/1000, cost))

    # Calculate consumption this month
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem(event.itemName), DateTime.now().withTimeAtStartOfDay().withDayOfMonth(1))))
    events.postUpdate("Gas_Use_Month", "{0:.3f}".format(used))
    gasUsage.log.info("This Month's Gas Usage [{0:.3f}]".format(used/1000))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Month_Cost", "{0:.2f}".format(cost))
    events.postUpdate("Gas_Use_Month_Summary", u"{0:.0f} m3, € {1:.2f}".format(used/1000, cost))

    # Calculate consumption this year
    used = float(str(PersistenceExtensions.deltaSince(ir.getItem(event.itemName), contractStart)))
    if used is None:
        used = float(str(event.itemState)) - 7374000
        gasUsage.log.info("Fix for missing year data, pre-fill [{}]".format(used))
    events.postUpdate("Gas_Use_Year", str(used))
    gasUsage.log.info("This Contract Year's Gas Usage [{0:.3f}]".format(used/1000))
    cost = used * GAS_PRICE_PER_DM3
    events.postUpdate("Gas_Use_Year_Cost", str(cost))
    events.postUpdate("Gas_Use_Year_Summary", u"{0:.0f} m3, € {1:.2f}".format(used/1000, cost))
