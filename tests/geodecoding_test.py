"""Test for geodecoding module."""
import unittest

import util.geodecoding


class GeodecodingTest(unittest.TestCase):
    """Geodecoding test."""

    def test_country_code(self):
        """Test obtaining country code by GPS coordinates."""

        countries = [
            {
                'coords': '47.8376698,35.1217301',
                'short_country_code': 'UA'},
            {
                'coords': '31.7481223,35.2149544',
                'short_country_code': 'IL'},
            {
                'coords': '-1.3149347,36.8237364',
                'short_country_code': 'KE'},
            {
                'coords': '-51.638731,-69.2187305',
                'short_country_code': 'AR'},
            {
                'coords': '34.9580867,138.0272817',
                'short_country_code': 'JP'}]

        for country in countries:
            with self.subTest(coords=country['coords'], expected_country_code=country['short_country_code']):
                obtained_country_code = util.geodecoding.gps_to_country_code(country['coords'])
                self.assertEqual(
                    obtained_country_code, country['short_country_code'],
                    "expected {} country code for coords {}, but {} got instead".format(
                        country['short_country_code'], country['coords'], obtained_country_code))

    def test_invalid_gps(self):
        """Test obtaining country code by invalid GPS coordinates."""
        invalid_coords = [
            '-1235.4568,1873.78977',
            '-0001.44,986.8',
            'onetwo,three,four']

        for coords in invalid_coords:
            with self.subTest(coords=coords), self.assertRaises(util.geodecoding.GeodecodingError):
                util.geodecoding.gps_to_country_code(coords)

    def test_non_country(self):
        """Test obtaining country code by GPS coordinates of non-country place."""
        non_countries = [
            '19.1352379,169.9914628',
            '-64.9219625,-59.6789551',
            '88.8398092,-178.5668534']
        for coords in non_countries:
            with self.subTest(coords=coords):
                obtained_country_code = util.geodecoding.gps_to_country_code(coords)
                self.assertEqual(
                    obtained_country_code, '',
                    "place with coords {} has code {}, but does not any country code expected".format(
                        coords, obtained_country_code))
