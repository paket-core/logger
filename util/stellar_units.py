"""Stellar assets unit handling."""
# number of decimals after decimal point
DEC = 7


def stroops_to_units(amount, numeric_representation=False):
    """
    Convert amount presented in stroops to units.
    :param int amount: Amount of stroops to be converted
    :param numeric_representation: If true, result will be returned as float number, otherwise - string
    """
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise TypeError

    amount = "{amount:0>{decimals}}".format(amount=amount, decimals=DEC)
    amount = "0.{}".format(amount) if len(amount) == DEC else "{}.{}".format(amount[:-DEC], amount[-DEC:])

    if numeric_representation:
        amount = float(amount)
    return amount


def units_to_stroops(amount, numeric_representation=False):
    """
    Convert amount presented in units to stroops.
    :param str amount: Amount of units to be converted
    :param numeric_representation: If true, result will be returned as integer number, otherwise - string
    """

    amount = _validate_and_prepare_units(amount)
    integer_part, fractional_part = str(amount).split('.')
    if integer_part != '0':
        amount = "{0}{1}".format(integer_part, fractional_part)
    else:
        striped = fractional_part.lstrip('0')
        leading_zeros_amount = len(fractional_part) - len(striped)
        trailing_zeros_amount = DEC - leading_zeros_amount - len(striped)
        amount = "{0}{1}".format(striped, '0' * trailing_zeros_amount)

    if numeric_representation:
        amount = int(amount)
    return amount


def _validate_and_prepare_units(units_amount):
    """
    Validate and prepare units for further conversions

    For conversions allowed only instances of `int`, `float` or `str`.
    For `int` and `float` uses string formatting with digital precision
    For 'str' check if digital point present and add it (with trailing zeros) in case it abcent.
    """
    if (
            not isinstance(units_amount, (str, float)) and
            not (isinstance(units_amount, int) and not isinstance(units_amount, bool))):
        raise TypeError

    if isinstance(units_amount, (int, float)):
        return "{amount:0.{decimals}f}".format(amount=units_amount, decimals=DEC)
    return units_amount if '.' in units_amount else "{}.{}".format(units_amount, '0' * DEC)
