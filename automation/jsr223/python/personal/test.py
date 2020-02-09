from core.rules import rule
from core.triggers import when

@rule("Test Rule")
@when("System started")
def testRule(event):
    if str(ir.getItem("Light_Scene_Bathroom").state) == "OFF":
        testRule.log.info("1. Bathroom switch is OFF")

    if items["Light_Scene_Bathroom"] == StringType("OFF"):
        testRule.log.info("2. Bathroom switch is OFF")

    if items.Light_Scene_Bathroom == StringType("OFF"):
        testRule.log.info("3. Bathroom switch is OFF")

    if items["Test_Item"] == ON:
        testRule.log.info("1. Test_Item is ON")        
    else:
        testRule.log.info("1. Test_Item is not ON (probably OFF)")

    if items.Test_Item == ON:
        testRule.log.info("2. Test_Item is ON")        
    else:
        testRule.log.info("2. Test_Item is not ON (probably OFF)")
