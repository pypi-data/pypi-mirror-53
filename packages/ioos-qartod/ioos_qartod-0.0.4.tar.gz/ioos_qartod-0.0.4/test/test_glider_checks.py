#!/usr/bin/env python
'''
test/test_glider_checks.py
'''

import numpy as np
import numpy.testing as npt
from ioos_qartod.qc_tests import gliders
import unittest


class TestGliderChecks(unittest.TestCase):
    def test_pressure_downcast(self):
        # Standard downcast
        pressure = np.array([0.0, 2.0, 2.1, 2.12, 2.3, 4.0, 14.2, 20.0], dtype='float32')
        flags = gliders.pressure_check(pressure)
        npt.assert_array_equal(flags, np.array([1, 1, 1, 1, 1, 1, 1, 1]))

    def test_pressure_upcast(self):
        # Standard upcast
        pressure = np.array([0.0, 2.0, 2.1, 2.12, 2.3, 4.0, 14.2, 20.0], dtype='float32')
        pressure = pressure[::-1]
        flags = gliders.pressure_check(pressure)
        npt.assert_array_equal(flags, np.array([1, 1, 1, 1, 1, 1, 1, 1]))

    def test_pressure_shallow(self):
        # Shallow profiles should be flagged if it's stuck or decreasing
        pressure = np.array([0.0, 2.0, 2.0, 1.99, 2.3, 2.4, 2.4, 2.5], dtype='float32')
        flags = gliders.pressure_check(pressure)
        npt.assert_array_equal(flags, np.array([1, 1, 3, 3, 1, 1, 3, 1]))
