'''
----------------------------------------------------------------------------------------------------
astro_sun_direction.py - Translate Sun azimuth to wind direction.
----------------------------------------------------------------------------------------------------
Changelog:
20200115 v01    Created initial script.
----------------------------------------------------------------------------------------------------
'''

from core.rules import rule
from core.triggers import when
from core.log import logging, LOG_PREFIX
import configuration
reload(configuration)
from configuration import LOG_PREFIX
from core.utils import postUpdateCheckFirst

log = logging.getLogger("{}.astro_azimuth".format(LOG_PREFIX))

#==================================================================================================
@rule("AstroSunPosition", description="Translate Sun Azimut degrees to Wind Direction", tags=["astro"])
@when("Item Astro_Sun_Azimuth changed")
@when("System started")
def update_sun_direction(event):

    wind_directions = {
        xrange(0, 12) : 'North',
        xrange(12, 34) : 'North-NorthEast',
        xrange(34, 57) : 'North-East',
        xrange(57, 79) : 'East-NorthEast',
        xrange(79, 102) : 'East',
        xrange(102, 125) : 'East-SouthEast',
        xrange(125, 147) : 'SouthEast',
        xrange(147, 170) : 'South-SouthEast',
        xrange(170, 192) : 'South',
        xrange(192, 215) : 'South-SouthWest',
        xrange(215, 237) : 'SouthWest',
        xrange(237, 259) : 'West-SouthWest',
        xrange(259, 283) : 'West',
        xrange(283, 305) : 'West-NorthWest',
        xrange(305, 327) : 'NorthWest',
        xrange(327, 349) : 'North-NorthWest',
        xrange(349, 366) : 'North'
    }

    azimuth = int(float(str(items.Astro_Sun_Azimuth)))
    for key in wind_directions:
        if azimuth in key:
            wind_direction = wind_directions[key]
            postUpdateCheckFirst("Astro_Sun_Direction", str(wind_direction))
            break
