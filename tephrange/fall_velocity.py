# -*- coding: utf-8 -*-
"""Functions for calculating terminal velocity of particles using different
methods."""

from travdist import atmos
import numpy as np

GRAVITY = atmos.G
ATM_DENSITY = atmos.ATM_DENSITY
ATM_VISCOSITY = atmos.ATM_VISCOSITY


def stokes(diameter,
           density=2300, atm_density=ATM_DENSITY, atm_viscosity=ATM_VISCOSITY):
    """
    Calculates terminal velocity of a particle of given diameter using
    Stokes' law.  Default values are for andesite at sea level.
    """

    velocity = (1/18.0) * (density - atm_density) / atm_viscosity * \
               GRAVITY * diameter**2
    return velocity


def ganser(diameter, sphericity=0.7,
           density=2300, atm_density=ATM_DENSITY, atm_viscosity=ATM_VISCOSITY):
    """
    Calculates terminal velocity of a particle of given diameter (m) and
    sphericity using the Ganser (1993) equation.  Default values are for 
    andesite at sea level, as used in Stevenson et al (2015).
    """

    # Set up internal constants
    k1 = 3 / (1 + 2*(sphericity**-0.5))
    k2 = 10**(1.8148*((-np.log10(sphericity))**0.5743))  # Note log10 here

    # Iteratively calculate terminal velocity
    velocity = stokes(diameter, density,
                      atm_density, atm_viscosity)  # First guess is Stokes'
    velocity_difference = 99999
    while abs(velocity_difference) > 0.000001:  # Usually < 15 iterations
        reynolds = _get_reynolds(diameter, velocity, atm_density, atm_viscosity)
        drag = (
            (24/(reynolds*k1*k2) *
            (1 + 0.1118*((reynolds*k1*k2)**0.6567))) +
            (0.4345 / (1 + (3305/(reynolds*k1*k2))))
            ) * k2
        new_velocity = np.sqrt((4 * diameter * GRAVITY *
                               (density - atm_density)) /
                               (3 * drag * atm_density))
        velocity_difference = velocity - new_velocity
        velocity = new_velocity
    return velocity


def white(diameter, density=2300, atm_density=ATM_DENSITY,
          atm_viscosity=ATM_DENSITY):
    """
    Calculates terminal velocity of a given diameter (m) using White (1974)
    equation.  Default values are for andesite at sea level.
    """

    # Set up internal constants
    c1 = 0.25
    c2 = 6.0

    # Iteratively calculate terminal velocity
    velocity = stokes(diameter, density,
                      atm_density, atm_viscosity)  # First guess is Stokes'
    velocity_difference = 99999
    while abs(velocity_difference) > 0.000001:
        reynolds = _get_reynolds(diameter, velocity, atm_density, atm_viscosity)
        drag = (c1 + (24/reynolds) + (c2 / (1 + np.sqrt(reynolds))))
        new_velocity = np.sqrt((4 * diameter * GRAVITY *
                               (density - atm_density)) /
                               (3 * drag * atm_density))
        velocity_difference = velocity - new_velocity
        velocity = new_velocity
    return velocity


def _get_reynolds(diameter, velocity,
                  atm_density=ATM_DENSITY, atm_viscosity=ATM_VISCOSITY):
    """
    Calculates Reynolds number for a falling particle of given diameter (m)
    and velocity.
    """
    reynolds = diameter * velocity * atm_density / atm_viscosity
    return reynolds

