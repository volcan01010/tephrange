# -*- coding: utf-8 -*-
"""Functions for calculating the density of an ash particle based upon the
size and composition."""

import numpy as np


def bp2003(diameter, rho_pumice=440, rho_glass=2300):
    """
    Return the density of particles of given diameter (m) based on the model
    of Bonadonna and Phillips (2003), which assumes a linear decrease (on
    the phi scale) from lithic at 8 microns (6 phi) to pumice at 2
    millimeters (-1 phi).

    Example values are:

    Rhyolite (default):
        Eruption: Askja 1875 Pumice: 440 kg/m3, Lithic: 2300 kg/m3
    Dacite:
        Eruption: Quizapú 1932  Pumice: 655 kg/m3, Lithic: 2400 kg/m3
    Andesite:
        Eruption: Hudson 1991  Pumice: 1000 kg/m3, Lithic: 2600 kg/m3

    :param diameter: Numpy array of particle diameters
    :return density: Numpy array of particle density in kg/m3.
    """
    diam_lithic = 7
    diam_pumice = -1

    diam_phi = -np.log2(diameter * 1000)
    if diam_phi > diam_lithic:
        return rho_glass
    elif diam_phi < diam_pumice:
        return rho_pumice
    else:
        diff_diam = diam_pumice - diam_lithic
        diff_rho = abs(rho_pumice - rho_glass)
        density = rho_glass - (((diam_phi - diam_lithic) /
                                diff_diam) * diff_rho)
    return density


def convert_to_solidity(density, rho_glass=2300, rho_atm=1.225):
    """
    Calculate the solidity of a particle given the bulk density (kg/m3)
    and the lithic density.  Default rho_glass corresponds to Askja
    rhyolite glass.

    :density: np.array of density values
    :return solidity: Proportion of particle volume occupied by solid.
    """
    # density = X*rho_glass + (1-X)*rho_air
    # X = (density - rho_air) / (rho_glass - rho_air)
    result = np.array(
        [single_solidity(x, rho_glass=rho_glass, rho_atm=rho_atm)
         for x in density])

    return result


def single_solidity(density, rho_glass=2300, rho_atm=1.225):
    if density > rho_glass:
        raise ValueError('Particle density ({}) is more than glass '
                         'density ({})'.format(density, rho_glass))
    if density < rho_atm:
        raise ValueError('Particle density ({}) is less than '
                         'atmosphere density ({})'.format(density,
                                                          rho_atm))
    return (density - rho_atm) / (rho_glass - rho_atm)
