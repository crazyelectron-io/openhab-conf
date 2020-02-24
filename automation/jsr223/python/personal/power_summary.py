'''
----------------------------------------------------------------------------------------------------
energy_power.py - Calculate the total and periodic sum and delta of power consumption.
----------------------------------------------------------------------------------------------------
Changelog:
20200128 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
import configuration
reload(configuration)
from configuration import powerPriceDict
from core.actions import PersistenceExtensions
from org.joda.time import DateTime

contractStart = DateTime.now().withTimeAtStartOfDay().withDayOfYear(15)  #Contract started at January 15. TODO: Move to configuration file

#==================================================================================================
@rule("Calculate Power Summary", description="Calculate the total and periodic sum and delta of power consumption", tags=["energy"])
@when("Item Power_Use_Total changed")
@when("Item Power_Use_T1_Total changed")
@when("Item Power_Use_T2_Total changed")
@when("Item Power_Ret_Total changed")
@when("Item Power_Ret_T1_Total changed")
@when("Item Power_Use_T2_Total changed")
def powerSummary(event):
    global contractStart
    if event.oldItemState is None:
        return
    else:
        events.postUpdate("DSMR_Watchdog", "ON")

    # Define variables
    usedHour = 0
    usedDay = 0
    usedMonth = 0
    usedYear = 0
    usedContract = 0
    returnedHour = 0
    returnedDay = 0
    returnedMonth = 0
    returnedYear = 0
    returnedContract = 0
    kWhPrice = float(powerPriceDict.get("T"+str(items["Power_Tariff"])).get("use_price"))

    # Calculate multiple periods of power consumption
    if not isinstance(ir.getItem("Power_Use_Total"), UnDefType):
        usedHour = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Use_Total"), DateTime.now().minusHours(1))))
        events.postUpdate("Power_Use_Hour", "{0:.3f}".format(usedHour))
        usedDay = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Use_Total"), DateTime.now().withTimeAtStartOfDay())))
        events.postUpdate("Power_Use_Day", "{0:.3f}".format(usedDay))
        usedMonth = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Use_Total"), DateTime.now().withTimeAtStartOfDay().withDayOfMonth(1))))
        usedYear = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Use_Total"), DateTime.now().withTimeAtStartOfDay().withMonthOfYear(1).withDayOfMonth(1))))
        usedContract = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Use_Total"), contractStart)))

    # Calculate multiple periods power return
    if not isinstance(ir.getItem("Power_Ret_Total"), UnDefType):
        returnedHour = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Ret_Total"), DateTime.now().minusHours(1))))
        events.postUpdate("Power_Ret_Hour", "{0:.3f}".format(returnedHour))
        returnedDay = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Ret_Total"), DateTime.now().withTimeAtStartOfDay())))
        events.postUpdate("Power_Ret_Day", "{0:.3f}".format(returnedDay))
        returnedMonth = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Ret_Total"), DateTime.now().withTimeAtStartOfDay().withDayOfMonth(1))))
        returnedYear = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Ret_Total"), DateTime.now().withTimeAtStartOfDay().withMonthOfYear(1).withDayOfMonth(1))))
        returnedContract = float(str(PersistenceExtensions.deltaSince(ir.getItem("Power_Ret_Total"), contractStart)))

    # Calculate last hour's power delta usage and price
    delta = usedHour - returnedHour
    deltaPrice = (usedHour * kWhPrice) - (returnedHour * kWhPrice)
    powerSummary.log.debug("Last hours power use/return/delta [{0:.3f}/{1:.3f}/{2:.3f}]; net cost [{3:.2f}]".format(usedHour, returnedHour, delta, deltaPrice))
    events.postUpdate("Power_Delta_Hour", "{0:.3f}".format(delta))
    events.postUpdate("Power_Delta_Hour_Cost", "{0:.2f}".format(deltaPrice))
    events.postUpdate("Power_Delta_Hour_Summary", u"{0:.3f} kWh, € {1:.2f}".format(delta/1000, deltaPrice))

    # Calculate today's power delta
    delta = usedDay - returnedDay
    deltaPrice = (usedDay * kWhPrice) - (returnedDay * kWhPrice)
    powerSummary.log.debug("Todays power use/return/delta [{0:.3f}/{1:.3f}/{2:.3f}]; net cost [{3:.2f}]".format(usedDay/1000, returnedDay/1000, delta/1000, deltaPrice))
    events.postUpdate("Power_Delta_Day", str(delta))
    events.postUpdate("Power_Delta_Day_Cost", str(deltaPrice))
    events.postUpdate("Power_Delta_Day_Summary", u"{0:.2f} kWh, € {1:.2f}".format(delta/1000, deltaPrice))

    # Calculate this month's power delta
    delta = usedMonth - returnedMonth
    deltaPrice = (usedMonth * kWhPrice) - (returnedMonth * kWhPrice)
    powerSummary.log.debug("This months power use/return/delta [{}/{}/{}]; net cost [{}]".format(usedMonth, returnedMonth, delta, deltaPrice))
    events.postUpdate("Power_Delta_Month", str(delta))
    events.postUpdate("Power_Delta_Month_Cost", str(deltaPrice))
    events.postUpdate("Power_Delta_Month_Summary", u"{0:.0f} kWh, € {1:.2f}".format(delta/1000, deltaPrice))

    # Calculate this year's power delta
    delta = usedYear - returnedYear
    deltaPrice = (usedYear * kWhPrice) - (returnedYear * kWhPrice)
    powerSummary.log.debug("This years power use/return/delta [{}/{}/{}]; net cost [{}]".format(usedYear, returnedYear, delta, deltaPrice))
    events.postUpdate("Power_Delta_Year", str(delta))
    events.postUpdate("Power_Delta_Year_Cost", str(deltaPrice))
    events.postUpdate("Power_Delta_Year_Summary", u"{0:.0f} kWh, € {1:.2f}".format(delta/1000, deltaPrice))

    # Calculate this contract period's power delta
    delta = usedContract - returnedContract
    deltaPrice = (usedContract * kWhPrice) - (returnedContract * kWhPrice)
    powerSummary.log.debug("This contract period's power use/return/delta [{}/{}/{}]; net cost [{}]".format(usedContract, returnedContract, delta, deltaPrice))
    events.postUpdate("Power_Delta_Contract", str(delta))
    events.postUpdate("Power_Delta_Contract_Cost", str(deltaPrice))
    events.postUpdate("Power_Delta_Contract_Summary", u"{0:.0f} kWh, € {1:.2f}".format(delta/1000, deltaPrice))
