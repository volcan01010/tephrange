import numpy as np
import unittest

from travdist import density


class TestBP2003(unittest.TestCase):
    def test_bp2003(self):
        rho_pumice = 500
        rho_glass = 2500
        diameter_microns = np.array([4, 125, 2000, 16000])
        diameter = diameter_microns / 1e6

        expected = [2500, 1500, 500, 500]
        for i, diam in enumerate(diameter):
            rho = density.bp2003(diam, rho_pumice=rho_pumice, rho_glass=rho_glass)
            e = expected[i]
            self.assertAlmostEqual(
                e, rho, places=5,
                msg="Density for {} metres was not {} ({})".format(
                    diam, e, rho))


class TestConvertToSolidity(unittest.TestCase):
    def setUp(self):
        self.rho_atm = 1
        self.rho_glass = 2001

    def test_too_dense(self):
        with self.assertRaises(ValueError):
            density.convert_to_solidity(np.array([9999]))

    def test_too_low_density(self):
        with self.assertRaises(ValueError):
            density.convert_to_solidity(np.array([0.1]))

    def test_solid(self):
        solidity = density.convert_to_solidity(np.array([2001]), rho_glass=self.rho_glass,
                                               rho_atm=self.rho_atm)
        self.assertEqual(solidity, 1,
                         "Solidity when density=rho_glass was not 1 {}".format(solidity))

    def test_air(self):
        solidity = density.convert_to_solidity(np.array([1]), rho_glass=self.rho_glass,
                                               rho_atm=self.rho_atm)
        self.assertEqual(solidity, 0,
                         "Solidity when density=rho_air was not 0 {}".format(solidity))

    def test_fifty_percent(self):
        solidity = density.convert_to_solidity(np.array([1001]), rho_glass=self.rho_glass,
                                               rho_atm=self.rho_atm)
        self.assertEqual(solidity, 0.5,
                         "Solidity when density=half_between_air_and_glass was not 0.5 {}".format(solidity))

if __name__ == '__main__':
    unittest.main()
