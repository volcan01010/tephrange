from mock import patch, MagicMock, sentinel, call
import unittest
from tephrange import particle
from tephrange import fall_velocity


class TestParticle(unittest.TestCase):
    @patch.object(particle.density, 'bp2003')
    def test_set_size_dependant_density(self, m_bp2003):
        # Arrange
        diameter = 0.0001
        rho_pumice = 555
        rho_glass = 2222
        expected = 9999
        m_bp2003.return_value = expected

        # Act
        p = particle.Particle(diameter)
        p.set_size_dependant_density(rho_pumice=rho_pumice,
                                     rho_glass=rho_glass)

        # Assert
        self.assertEqual(
            p.density, expected,
            "Particle density was not change to {} ({}).".format(expected,
                                                                 p.density))
        m_bp2003.assert_called_once_with(diameter,
                                         rho_pumice=rho_pumice,
                                         rho_glass=rho_glass)

    def test_update_travel_history(self):
        # Arrange
        diameter = 0.0001
        p = particle.Particle(diameter)
        p.current_altitude = 1
        p.current_travel_time = 2
        p.current_distance = 4

        # Act
        p._update_travel_history()

        # Assert
        self.assertEqual(p.altitude, [1],
                         "Current altitude not appended to altitude list")
        self.assertEqual(p.travel_time, [2],
                         "Current travel_time not appended to travel_time"
                         " list")
        self.assertEqual(p.distance, [4],
                         "Current distance not appended to distance list")

    def test_calc_fall_time_above_altitude(self):
        # Arrange
        expected_time = 1
        expected_distance = 999
        p = particle.Particle(0.0001)
        p.current_altitude = 8848

        # Act
        t, hd = p._calc_fall_time_and_distance(123, 123, 999)

        # Assert
        self.assertEqual(expected_time, t,
                         "Fall time was not {} ({})".format(expected_time, t))
        self.assertEqual(expected_distance, hd,
                         "Fall time was not {} ({})".format(expected_distance,
                                                            hd))

    def test_calc_fall_time_below_altitude(self):
        # Arrange
        expected_time = 0.5
        expected_distance = 250
        p = particle.Particle(0.0001)
        p.current_altitude = 5

        # Act
        t, hd = p._calc_fall_time_and_distance(10, 10, 500)

        # Assert
        self.assertEqual(expected_time, t,
                         "Fall time was not {} ({})".format(expected_time, t))
        self.assertEqual(expected_distance, hd,
                         "Fall time was not {} ({})".format(expected_distance,
                                                            hd))

    def test_get_fall_velocity_invalid(self):
        # Arrange
        p = particle.Particle(0.0001)

        # Act and assert
        with self.assertRaises(ValueError):
            p.get_fall_velocity(100, 100, 'invalid')

    @patch.object(particle.fall_velocity, 'ganser')
    def test_get_fall_velocity_ganser(self, m_ganser):
        # Arrange
        m_ganser.return_value = 9999
        diameter = 0.0001
        atm_density = 123
        atm_viscosity = 456
        p = particle.Particle(diameter)
        p.sphericity = 0.5
        p.density = 5678

        # Act
        v_terminal = p.get_fall_velocity(atm_density=atm_density,
                                         atm_viscosity=atm_viscosity,
                                         velocity_function='ganser')

        # Assert
        self.assertEqual(v_terminal, 9999,
                         "v_terminal was not 9999 ({})".format(v_terminal))
        m_ganser.assert_called_once_with(diameter=diameter,
                                         sphericity=0.5,
                                         density=5678,
                                         atm_density=atm_density,
                                         atm_viscosity=atm_viscosity)

    @patch.object(particle.fall_velocity, 'stokes')
    def test_get_fall_velocity_stokes(self, m_stokes):
        # Arrange
        m_stokes.return_value = 9999
        diameter = 0.0001
        atm_density = 123
        atm_viscosity = 456
        p = particle.Particle(diameter)
        p.sphericity = 0.5
        p.density = 5678

        # Act
        v_terminal = p.get_fall_velocity(atm_density=atm_density,
                                         atm_viscosity=atm_viscosity,
                                         velocity_function='stokes')

        # Assert
        self.assertEqual(v_terminal, 9999,
                         "v_terminal was not 9999 ({})".format(v_terminal))
        m_stokes.assert_called_once_with(diameter=diameter,
                                         density=5678,
                                         atm_density=atm_density,
                                         atm_viscosity=atm_viscosity)

    @patch.object(particle.fall_velocity, 'stokes')
    def test_get_fall_velocity_stokes_sea_level(self, m_stokes):
        # Arrange
        m_stokes.return_value = sentinel.velocity
        diameter = 0.0001
        atm_density = fall_velocity.ATM_DENSITY
        atm_viscosity = fall_velocity.ATM_VISCOSITY
        p = particle.Particle(diameter)
        p.sphericity = 0.5
        p.density = sentinel.density

        # Act
        v_terminal = p.get_fall_velocity(atm_density=atm_density,
                                         atm_viscosity=atm_viscosity,
                                         velocity_function='stokes_sea_level')

        # Assert
        self.assertEqual(v_terminal, sentinel.velocity,
                         "v_terminal was not sentinel.velocity ({})".format(v_terminal))
        m_stokes.assert_called_once_with(diameter=diameter,
                                         density=sentinel.density,
                                         atm_density=atm_density,
                                         atm_viscosity=atm_viscosity)

    @patch.object(particle.fall_velocity, 'white')
    def test_get_fall_velocity_white(self, m_white):
        # Arrange
        m_white.return_value = 9999
        diameter = 0.0001
        atm_density = 123
        atm_viscosity = 456
        p = particle.Particle(diameter)
        p.sphericity = 0.5
        p.density = 5678

        # Act
        v_terminal = p.get_fall_velocity(atm_density=atm_density,
                                         atm_viscosity=atm_viscosity,
                                         velocity_function='white')

        # Assert
        self.assertEqual(v_terminal, 9999,
                         "v_terminal was not 9999 ({})".format(v_terminal))
        m_white.assert_called_once_with(diameter=diameter,
                                        density=5678,
                                        atm_density=atm_density,
                                        atm_viscosity=atm_viscosity)

    @patch.object(particle.atmos, 'get_density', return_value=sentinel.density)
    @patch.object(particle.atmos, 'get_viscosity', return_value=sentinel.visc)
    def test_calc_step_movement(self, m_viscosity, m_density):
        # Arrange
        diameter = 0.0001
        p = particle.Particle(diameter)
        p.current_altitude = sentinel.altitude
        p.get_fall_velocity = MagicMock()
        p.get_fall_velocity.return_value = sentinel.v_terminal
        p._calc_fall_time_and_distance = MagicMock()
        p._calc_fall_time_and_distance.return_value = (sentinel.fall_time,
                                                       sentinel.hd)

        # Act
        fall_time, hd = p._calc_step_movement('ganser', sentinel.fall_step,
                                              sentinel.windspeed)

        # Assert
        m_density.assert_called_once_with(sentinel.altitude)
        m_viscosity.assert_called_once_with(sentinel.altitude)
        p.get_fall_velocity.assert_called_once_with(
            sentinel.density, sentinel.visc, 'ganser')
        p._calc_fall_time_and_distance.assert_called_once_with(
            sentinel.fall_step, sentinel.v_terminal, sentinel.windspeed)
        self.assertEqual((fall_time, hd), (sentinel.fall_time, sentinel.hd),
                         "Incorrect time and/or distance returned")

    def test_calculate_distance_once_landed(self):
        # Arrange
        p = particle.Particle(sentinel.diameter)
        expected_distance = 1000
        p.current_distance = expected_distance * 1000

        # Act
        distance = p.calculate_distance(release_height=0)

        # Assert
        self.assertEqual(distance, expected_distance,
                         "Travel distance changed from {} ({})".format(
                             expected_distance, distance))

    @patch.object(particle.Particle, '_calc_step_movement',
                  return_value=(sentinel.ft, sentinel.hd))
    def test_calculate_distance(self, m_step_movement):
        # Arrange
        p = particle.Particle(sentinel.diam)
        m_step_movement.return_value = (1, 1000)

        # Act
        distance = p.calculate_distance(release_height=30,
                                        windspeed=sentinel.ws,
                                        fall_step=10,
                                        velocity_function=sentinel.func)

        # Assert
        self.assertEqual(distance, 3,
                         "Particle did not travel 3 km ({})".format(distance))
        m_step_movement.assert_has_calls(
            [call(sentinel.func, 10, sentinel.ws)])


if __name__ == '__main__':
    unittest.main()
