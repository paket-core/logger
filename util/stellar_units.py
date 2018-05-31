"""Stellar assets unit handling."""
# number of decimals after decimal point
DEC = 7


def stroops_to_units(amount):
    """
    Convert amount presented in stroops to units.
    :param int amount: Amount of stroops to be converted
    """
    if not isinstance(amount, int):
        raise TypeError

    amount = '{amount:0>{decimals}}'.format(amount=amount, decimals=DEC)
    amount = '0.{}'.format(amount) if len(amount) == DEC else '{}.{}'.format(amount[:-DEC], amount[-DEC:])
    return amount


def units_to_stroops(amount):
    """
    Convert amount presented in units to stroops.
    :param str amount: Amount of units to be converted
    """
    if not isinstance(amount, str) and not isinstance(amount, float):
        raise TypeError

    integer_part, fractional_part = str(amount).split('.')
    if integer_part != '0':
        amount = '{0}{1:0<{decimals}}'.format(integer_part, fractional_part, decimals=DEC)
    else:
        striped = fractional_part.lstrip('0')
        leading_zeros_amount = len(fractional_part) - len(striped)
        trailing_zeros_amount = DEC - leading_zeros_amount - len(striped)
        amount = '{0}{1}'.format(striped, '0' * trailing_zeros_amount)
    return amount
