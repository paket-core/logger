"""Reverse geocoding utils."""
import os

import requests

GOOGLE_API_KEY = os.environ.get('PAKET_GOOGLE_API_KEY')
URL = 'https://maps.googleapis.com/maps/api/geocode/json'
RESULT_TYPE = 'country'
PARAMS = {
    'language': 'en',
    'result_type': RESULT_TYPE,
    'key': GOOGLE_API_KEY}


class GeodecodingError(Exception):
    """Geodecoding error."""


def gps_to_country_code(gps_coords):
    """Obtain short country code by GPS coordinates."""
    PARAMS['latlng'] = gps_coords
    response = requests.get(URL, PARAMS).json()

    if response['status'] == 'ZERO_RESULTS':
        return ''

    if response['status'] != 'OK':
        raise GeodecodingError(response['error_message'])

    result = next((result for result in response['results'] if RESULT_TYPE in result['types']), None)
    country_code = result['address_components'][0]['short_name'] if result is not None else ''
    return country_code
