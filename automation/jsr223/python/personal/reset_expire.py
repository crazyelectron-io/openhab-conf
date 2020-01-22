# --------------------------------------------------------------------------------------------------
# reset_expire.py - Reset the expire binding that are in group gResetExpire
#
# 20200120 v01  Initial version.
# --------------------------------------------------------------------------------------------------

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX

log = logging.getLogger("{}.rst_expire".format(LOG_PREFIX))


@rule("Reset Expire Binding Timers", description="Sends an update to all members of gResetExpire of their restored state", tags=["admin"])
@when("System started")
def reset_expire(event):
    log.info("Restarting Expire binding Timers")
    for timer in ir.getItem("gResetExpire").members:
        events.postUpdate(timer, timer.getState())
