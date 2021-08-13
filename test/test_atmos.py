from mock import patch, sentinel
import unittest

from travdist import atmos

class TestAtmos(unittest.TestCase):
    def test_celcius(self):
        # Arrange, act
        expected = 2
        c = atmos.celcius(275.15)

        # Assert
        self.assertEqual(c, expected,
                         "Celcius result was not {} ({})".format(expected, c))

    @patch.object(atmos, 'get_atmos_temp_press', return_value=(274.15, 0))
    def test_viscosity_above_freezing(self, m_atmos_temp_press):
        # Arrange
        expected = (1.718 + 0.0049) * 1e-5

        # Act
        viscosity = atmos.get_viscosity(sentinel.alt)

        # Assert
        m_atmos_temp_press.assert_called_once_with(sentinel.alt)
        self.assertEqual(expected, viscosity)

    @patch.object(atmos, 'get_atmos_temp_press', return_value=(272.15, 0))
    def test_viscosity_below_freezing(self, m_atmos_temp_press):
        # Arrange
        expected = (1.718 - 0.0049 - 1.2e-5) * 1e-5

        # Act
        viscosity = atmos.get_viscosity(sentinel.alt)

        # Assert
        m_atmos_temp_press.assert_called_once_with(sentinel.alt)
        self.assertEqual(expected, viscosity)

    def test_atmos_temp_press(self):
        # Arrange
        # ICAO defined values, see code for details.  Tuple is temp, press
        icao_values = {0: (15, 1013.25),
                       11000: (-56.5, 226.00),
                       20000: (-56.5, 54.70),
                       32000: (-44.5, 8.68)}

        # Act, assert
        for altitude, (icao_t, icao_p) in icao_values.items():
            t, p = atmos.get_atmos_temp_press(altitude)
            t = atmos.celcius(t)
            p /= 100.0
            self.assertAlmostEqual(
                t, icao_t, 1,
                "Temperature ({}) does not match ICAO ({})".format(t, icao_t))
            self.assertAlmostEqual(
                p, icao_p, 0,
                "Pressure ({}) does not match ICAO ({})".format(p, icao_p))

    def test_get_density(self):
        # Arrange
        # ICAO defined values
        icao_values = {0: 1.2250,
                       5000: 0.736429,
                       11000: 0.364801,
                       20000: 0.0889097,
                       32000: 0.0135551}

        # Act and assert
        for altitude in icao_values:
            density = atmos.get_density(altitude)
            # Matching to within 2 decimal places is close enough
            self.assertAlmostEqual(icao_values[altitude], density,
                                   2)


if __name__ == '__main__':
    unittest.main()
