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
from core.actions import PersistenceExtensions
from org.joda.time import DateTime
import configuration
reload(configuration)
from configuration import powerPriceDict

#===================================================================================================
@rule("Calculate Solar Summary", description="Calculate the solarpanel production prices and totals", tags=["energy","solar"])
@when("Item Solar_Prod_Day changed")
@when("Item Solar_Prod_Month changed")
@when("Item Solar_Prod_Year changed")
def solarSummary(event):
    if isinstance(items[event.itemName], UnDefType) or event.oldItemState is None:
        return
    else:
        solarSummary.log.info("Calculate Solar Summary, triggered by [{}]".format(event.itemName))

    price = powerPriceDict.get("T"+str(items["Power_Tariff"])).get("return_price")
    cost = float(event.itemState.toString()) * float(price)
    summary = "{:.1f} kWh, EUR {:.2f}".format(float(str(event.itemState))/1000, cost)
    costItem = ir.getItem(event.itemName + "_Cost")
    events.postUpdate(costItem, str(cost))
    summaryItem = ir.getItem(event.itemName + "_Summary")
    events.postUpdate(summaryItem.name, summary)

    if (str(event.itemName) == "Solar_Prod_Day"):
        solarDelta = float(str(PersistenceExtensions.deltaSince(ir.getItem("Solar_Prod_Day"), DateTime.now().minusHours(1))))
        solarSummary.log.info("Calculate last hours solar production: [{}]".format(solarDelta))
        events.postUpdate("Solar_Prod_Hour", str(solarDelta))
        cost = float(solarDelta) * float(price)
        summary = "{:.1f} kWh, EUR {:.2f}".format(solarDelta/1000, cost)
        events.postUpdate("Solar_Prod_Hour_Summary", summary)
