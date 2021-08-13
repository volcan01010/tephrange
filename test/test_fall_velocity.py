import unittest
from travdist import fall_velocity as fv


class TestGanser(unittest.TestCase):
    def test_sphericity_07(self):
        """
        Test that Ganser fall velocity produces numbers within tolerance.
        Expected values calculated by Frances Beckett using FORTRAN.
        """
        density = 2300
        atm_density = 1.2
        atm_viscosity = 1.82e-5

        d_microns = [10, 25, 50, 100]
        d_metres = [d / 1.0e6 for d in d_microns]
        expected = [0.00605, 0.0365, 0.1318761, 0.4035077]
        for i, d in enumerate(d_metres):
            velocity = fv.ganser(d, sphericity=0.7, density=density,
                                 atm_density=atm_density,
                                 atm_viscosity=atm_viscosity)
            proportion = velocity / expected[i]
            tol = 0.005
            within_tolerance = (1.0 - tol) < proportion < (1.0 + tol)
            self.assertTrue(
                within_tolerance,
                'Velocity for {} microns differs by more than {}% ({}).\n'
                'Calculated: {}\nExpected: {}'.format(1e6 * d,
                                                      100 * tol,
                                                      100 * (1 - proportion),
                                                      velocity,
                                                      expected[i]))


class TestStokes(unittest.TestCase):
    def test_stokes(self):
        """
        Test that Stokes' fall velocity produces numbers within tolerance.
        """
        density = 2300
        atm_density = 1.2
        atm_viscosity = 1.82e-5

        d_microns = [10, 25, 50, 100]
        d_metres = [d / 1.0e6 for d in d_microns]
        expected = [0.0068814, .04301, 0.17204, 0.68814]
        for i, d in enumerate(d_metres):
            velocity = fv.stokes(d, density=density,
                                 atm_density=atm_density,
                                 atm_viscosity=atm_viscosity)
            proportion = velocity / expected[i]
            tol = 0.005
            within_tolerance = (1.0 - tol) < proportion < (1.0 + tol)
            self.assertTrue(
                within_tolerance,
                'Velocity for {} microns differs by more than {}% ({}).\n'
                'Calculated: {}\nExpected: {}'.format(1e6 * d,
                                                      100 * tol,
                                                      100 * (1 - proportion),
                                                      velocity,
                                                      expected[i]))


@unittest.skip("Waiting for 'true' results to compare with")
class TestWhite(unittest.TestCase):
    def test_stokes(self):
        """
        Test that White fall velocity produces numbers within tolerance.
        """
        density = 2300
        atm_density = 1.2
        atm_viscosity = 1.82e-5

        d_microns = [10, 25, 50, 100]

        d_metres = [d / 1.0e6 for d in d_microns]
        expected = [0.0068814, .04301, 0.17204, 0.68814]
        for i, d in enumerate(d_metres):
            velocity = fv.white(d, density=density,
                                 atm_density=atm_density,
                                 atm_viscosity=atm_viscosity)
            proportion = velocity / expected[i]
            tol = 0.005
            within_tolerance = (1.0 - tol) < proportion < (1.0 + tol)
            self.assertTrue(
                within_tolerance,
                'Velocity for {} microns differs by more than {}% ({}).\n'
                'Calculated: {}\nExpected: {}'.format(1e6 * d,
                                                      100 * tol,
                                                      100 * (1 - proportion),
                                                      velocity,
                                                      expected[i]))
if __name__ == '__main__':
    unittest.main()
