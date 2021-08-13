# -*- coding: utf-8 -*-
"""
An class to represent a falling ash particle.

Created on Wed Sep  2 15:00:03 2015

@author: jsteven5
"""
from travdist import atmos
from travdist import density
from travdist import fall_velocity


class Particle:
    """An ash particle that can calculate terminal velocity and travel
    distance in a simple wind field."""

    def __init__(self, diameter, sphericity=0.7, particle_density=2300):
        """Set the particle up with internal and external parameters."""
        # Internal
        self.diameter = diameter
        self.sphericity = sphericity
        self.density = particle_density

        # External
        self.altitude = []
        self.travel_time = []
        self.distance = []
        self.current_altitude = 0
        self.current_travel_time = 0
        self.current_distance = 0

    def set_size_dependant_density(self,  rho_pumice=440, rho_glass=2300):
        """Replace the default density with a size dependant function based
        on Bonadonna and Phillips (2003).  Default values correspond to
        Askja 1875 tephra.
        :param rho_pumice: Density of pumice in kg/m3
        :param rho_glass: Density of solid glass in kg/m3"""
        self.density = density.bp2003(self.diameter,
                                      rho_pumice=rho_pumice,
                                      rho_glass=rho_glass)

    def _update_travel_history(self):
        """
        Append current state to lists of past altitude, travel time and
        distance.
        """
        self.altitude.append(self.current_altitude)
        self.travel_time.append(self.current_travel_time)
        self.distance.append(self.current_distance)

    def calculate_distance(self, release_height=10000, windspeed=10,
                           fall_step=10, velocity_function='ganser'):
        """Loop through fall steps calculating travel distance with each
        step, for a given self instance.
        :param self: Particle instance
        :param release_height: Release height in metres
        :param windspeed: Windspeed in metres per second
        :param fall_step: Step size for fall calculation in metres
        :param velocity_function: Function used to calculate velocity"""

        self.current_altitude = release_height

        while self.current_altitude > 0:
            # Update internal history parameters
            self._update_travel_history()

            # Calculate movement in this step
            fall_time, horizontal_distance = self._calc_step_movement(
                velocity_function, fall_step, windspeed)

            # Update current parameters
            self.current_altitude -= fall_step
            self.current_travel_time += fall_time
            self.current_distance += horizontal_distance

        # Final update of internal parameters
        self._update_travel_history()

        return self.current_distance / 1000.0

    def _calc_step_movement(self, velocity_function, fall_step,
                            windspeed):
        """
        Calculate how far the particle falls and travels horizontally in
        this step.
        :param velocity_function: String name of velocity function
        :param fall_step: Fall step in metres
        :param windspeed: Windspeed in metres per second
        :return: fall_time, horizontal distance
        """
        # Get atmosphere conditions
        atm_density = atmos.get_density(self.current_altitude)
        atm_viscosity = atmos.get_viscosity(self.current_altitude)

        # Calculate terminal velocity
        v_terminal = self.get_fall_velocity(atm_density, atm_viscosity,
                                            velocity_function)

        # Calculate fall time and distance
        fall_time, horizontal_distance = self._calc_fall_time_and_distance(
            fall_step, v_terminal, windspeed)

        return fall_time, horizontal_distance

    def _calc_fall_time_and_distance(self, fall_step, v_terminal, windspeed):
        """
        Calculate the time taken to fall by the fall_step and the
        horizontal distance transported in that time.
        :param fall_step: Fall step in metres
        :param v_terminal: Terminal velocity in metres per second
        :param windspeed: Windspeed in metres per second
        :return: fall_time, horizontal_distance
        """
        if fall_step > self.current_altitude:
            fall_step = self.current_altitude
        fall_time = fall_step / v_terminal
        horizontal_distance = windspeed * fall_time

        return fall_time, horizontal_distance

    def get_fall_velocity(self, atm_density, atm_viscosity, velocity_function):
        """
        Calculate fall velocity in metres per second.
        :param atm_density: Atmospheric density in kg/m3
        :param atm_viscosity: Atmospheric viscosity
        :param velocity_function: Function used to calculate velocity
        :return: terminal velocity of particle
        """
        # Get fall velocity
        if velocity_function == 'ganser':
            v_terminal = fall_velocity.ganser(diameter=self.diameter,
                                              sphericity=self.sphericity,
                                              density=self.density,
                                              atm_density=atm_density,
                                              atm_viscosity=atm_viscosity)
        elif velocity_function == 'stokes':
            v_terminal = fall_velocity.stokes(diameter=self.diameter,
                                              density=self.density,
                                              atm_density=atm_density,
                                              atm_viscosity=atm_viscosity)
        elif velocity_function == 'stokes_sea_level':
            v_terminal = fall_velocity.stokes(
                diameter=self.diameter, density=self.density,
                atm_density=fall_velocity.ATM_DENSITY,
                atm_viscosity=fall_velocity.ATM_VISCOSITY)
        elif velocity_function == 'white':
            v_terminal = fall_velocity.white(diameter=self.diameter,
                                             density=self.density,
                                             atm_density=atm_density,
                                             atm_viscosity=atm_viscosity)
        else:
            msg =('Velocity function must be ganser, stokes,'
                  ' stokes_sea_level or white. {} given.')
            raise ValueError(msg.format(velocity_function))

        return v_terminal
