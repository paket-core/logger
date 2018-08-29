"""Test for distance module"""
import unittest

import util.distance


class DistanceTest(unittest.TestCase):
    """"""

    def test_distance(self):
        from_location = '52.447240,13.416683'
        to_location = '49.227132,31852766'
        distance = util.distance.haversine(from_location, to_location)
