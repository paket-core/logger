"""Stellar assets unit handling."""
import decimal

SCALE_FACTOR = 10 ** 7


def stroops_to_units(amount, str_representation=True):
    """Convert amount presented in stroops to units
    :param int amount: Amount of stroops to be converted
    :param bool str_representation: If given returns string representation of result value. Otherwise returns float
    """
    units = decimal.Decimal(amount) / decimal.Decimal(SCALE_FACTOR)
    if str_representation:
        return '{:.7f}'.format(units)
    return float(units)


def units_to_stroops(amount, str_representation=True):
    """Convert amount presented in units to stroops
    :param str amount: Amount of units to be converted
    :param bool str_representation: If given returns string representation of result value. Otherwise returns int
    """
    units = decimal.Decimal(amount) * decimal.Decimal(SCALE_FACTOR)
    if str_representation:
        return str((int(units)))
    return int(units)


def add_units(first, second, str_representation=True):
    """Add two units"""
    result = decimal.Decimal(first) + decimal.Decimal(second)
    if str_representation:
        return '{:.7f}'.format(result)
    return float(result)
