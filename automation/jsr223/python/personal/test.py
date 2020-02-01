from core.rules import rule
from core.triggers import when
from core.log import logging
import configuration
reload(configuration)
from configuration import LOG_PREFIX

#===================================================================================================
@rule("Test Rule", description="Test scope issues in scripted automation", tags=["test"])
#@when("Time cron 0 */10 * * * ?")
@when("Item Test_Item changed")
@when("System started")
def testRule(event):
    testRule.log = logging.getLogger("{}.testRule".format(LOG_PREFIX))

    if "Test_Item2" in items:
        testRule.log.info("Item [Test_Item2] exists in registry.")
    else:
        testRule.log.info("Item [Test_Item2] not found in registry.")
    
    if items["Test_Item"] == StringType("Test"):
        testRule.log.info("State of [Test_Item] is 'Test'")
    testRule.log.info("Accessed state of [Test_Item] using 'items[testitem]'")

    if items.Test_Item == StringType("Test"):
        testRule.log.info("State of [Test_Item] is still 'Test'")
    testRule.log.info("Accessed state of [Test_Item] using 'items.Test_Item'")
