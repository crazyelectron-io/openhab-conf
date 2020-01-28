'''
----------------------------------------------------------------------------------------------------
energy_solar.py - Calculate the solarpanel production price and totals summary.
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


log = logging.getLogger("{}.dsmr_solar".format(LOG_PREFIX))


#===================================================================================================
@rule("SolarSummary", description="Calculate the solarpanel production price and totals summary", tags=["energy","solar"])
@when("Item Solar_Prod_Day changed")
@when("Item Solar_Prod_Month changed")
@when("Item Solar_Prod_Year changed")
def calc_solar_power_summary(event):
    if event.oldItemState is None:
        return

    price = powerPriceDict.get("T"+str(items.Power_Tariff)).get("return_price")
    log.debug("Power price [{}] is now [{}]".format("T"+str(items.Power_Tariff), price))

    cost = float(event.itemState.toString()) * float(price)
    log.debug("Solar revenue is now [{}]".format(cost))

    summary = "{} kWh, EUR {}".format(float(str(event.itemState))/1000, cost/100)
    log.debug("Solar summary [{}]".format(summary))

    costItem = ir.getItem(event.itemName + "_Cost")
    events.postUpdate(costItem, str(cost))

    summaryItem = ir.getItem(event.itemName + "_Summary")
    events.postUpdate(summaryItem.name, summary)
