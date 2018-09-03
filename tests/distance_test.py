"""Test for distance module"""
import unittest

import util.distance


class DistanceTest(unittest.TestCase):
    """Test for distance calculations."""

    def test_distance(self):
        from_location = '47.858048,35.104131'
        to_location = '47.834367,35.147932'
        expected_distance = 4.19
        deviation = 0.5
        distance = util.distance.haversine(from_location, to_location)
        self.assertTrue(
            expected_distance + deviation > distance > expected_distance - deviation,
            'expected result: {}; given result: {}'.format(expected_distance, distance))
