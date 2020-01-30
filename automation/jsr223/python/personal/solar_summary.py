'''
----------------------------------------------------------------------------------------------------
solar_summary.py - Calculate the solarpanel production price and totals summary.
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
from configuration import LOG_PREFIX, powerPriceDict

#===================================================================================================
@rule("Calculate Solar Summary", description="Calculate the solarpanel production prices and totals", tags=["energy","solar"])
@when("Item Solar_Prod_Day changed")
@when("Item Solar_Prod_Month changed")
@when("Item Solar_Prod_Year changed")
def solarSummary(event):
    if event.oldItemState is None:
        return

    solarSummary.log = logging.getLogger("{}.solarSummary".format(LOG_PREFIX))

    price = powerPriceDict.get("T"+str(ir.getItem("Power_Tariff").state)).get("return_price")
    solarSummary.log.debug("Power price [{}] is now [{}]".format("T"+str(ir.getItem("Power_Tariff").state), price))

    cost = float(event.itemState.toString()) * float(price)
    solarSummary.log.debug("Solar revenue is now [{}]".format(cost))

    summary = "{} kWh, EUR {}".format(float(str(event.itemState))/1000, cost/100)
    solarSummary.log.debug("Solar summary [{}]".format(summary))

    costItem = ir.getItem(event.itemName + "_Cost")
    events.postUpdate(costItem, str(cost))

    summaryItem = ir.getItem(event.itemName + "_Summary")
    events.postUpdate(summaryItem.name, summary)
