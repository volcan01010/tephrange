# -*- coding: utf-8 -*-
"""Functions for calculating the properties of a standard atmosphere at
a given altitude."""

import numpy as np

# Define physics parameters (in SI units):
G = 9.80665  # Acceleration due to gravity.
ATM_GAS_CONSTANT = 287.05  # Specific gas constant for dry air.
ATM_DENSITY = 1.2250  # Atmospheric density at sea level
ATM_VISCOSITY = 1.7915e-5  # Atmospheric viscosity at sea level


def celcius(temperature):
    """Converts a temperature from degrees Kelvin to degrees Celcius."""
    return temperature - 273.15


def get_viscosity(altitude):
    """Calculates the dynamic viscosity of the atmosphere at a
    given altitude (m) using the ICAO standard atmosphere."""
    temp = get_atmos_temp_press(altitude)[0]

    # Dynamic viscosity calculation from NAME Physics.f90
    if temp > 273.15:
        viscosity = (1.718 + 0.0049*(temp - 273.15)) * 1e-5
    else:
        viscosity = (1.718 + 0.0049*(temp - 273.15) -
                     1.2e-5*(temp-273.15)**2) * 1e-5

    return viscosity


def get_density(altitude):
    """Calculates the density of the atmosphere at a given altitude (m)
    using the ICAO standard atmosphere."""
    temp, pressure = get_atmos_temp_press(altitude)
    atm_density = pressure / (ATM_GAS_CONSTANT * temp)
    return atm_density


def get_atmos_temp_press(altitude):
    """Calculates temperature and pressure of the atmosphere at a given
    altitude (m) using the ICAO standard atmosphere."""
    # Define internal constants
    temp0km = 288.15  # Temperature at 0km above mean sea level (K).
    temp11km = 216.65  # Temperature at 11km above mean sea level (K).
    temp20km = 216.65  # Temperature at 20km above mean sea level (K).
    lapse_rate_below_11km = 0.0065  # Lapse rate from 0 to 11km above mean sea level.
    lapse_rate_above_20km = -0.001  # Lapse rate at more than 20km above mean sea level.
    pressure0km = 101325  # Pressure at mean sea level (Pa).

    # Calculate anchor pressure levels
    pressure11km = pressure0km * \
                   (1 - lapse_rate_below_11km*11000 / temp0km) ** \
                   (G / (ATM_GAS_CONSTANT*lapse_rate_below_11km))
    pressure20km = pressure11km * np.exp(-G * 9000 /
                                         (ATM_GAS_CONSTANT*temp11km))

    # Interpolate between levels
    if altitude < 11000:
        pressure = pressure0km * \
                   (1 - lapse_rate_below_11km * altitude / temp0km) ** \
                   (G / (ATM_GAS_CONSTANT*lapse_rate_below_11km))
        temp = temp0km - lapse_rate_below_11km * altitude
    elif altitude < 20000:
        pressure = pressure11km * np.exp(-G * (altitude - 11000) /
                                         (ATM_GAS_CONSTANT*temp11km))
        temp = temp11km
    else:
        pressure = pressure20km * \
                           (1 - lapse_rate_above_20km * \
                           (altitude - 20000) / temp20km) ** \
                           (G / (ATM_GAS_CONSTANT*lapse_rate_above_20km)
                           )
        temp = temp20km - lapse_rate_above_20km * (altitude - 20000)

    return temp, pressure
