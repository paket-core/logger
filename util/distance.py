"""Distance util"""
from math import radians, cos, sin, asin, sqrt

# Earth radius in kilometers
EARTH_RADIUS = 6371


def haversine(from_location, to_location):
    """
    Great-circle distance between two points on a sphere given their longitudes and latitudes
    https://en.wikipedia.org/wiki/Haversine_formula
    ---
    :param str from_location: GPS coordinates of location from which distance will be calculated
    :param str to_location: GPS coordinates of location to which distance will be calculated
    :return float: distance in kilometers between two points
    """
    from_latitude, from_longitude = (float(value) for value in from_location.split(','))
    to_latitude, to_longitude = (float(value) for value in to_location.split(','))

    # convert all latitudes/longitudes from decimal degrees to radians
    from_latitude, from_longitude, to_latitude, to_longitude = map(
        radians, (from_latitude, from_longitude, to_latitude, to_longitude))

    # calculate haversine
    latitude = to_latitude - from_latitude
    longitude = to_longitude - from_longitude
    haversine_value = sin(latitude * 0.5) ** 2 + cos(from_latitude) * cos(to_latitude) * sin(longitude * 0.5) ** 2
    distance = 2 * EARTH_RADIUS * asin(sqrt(haversine_value))
    return distance
