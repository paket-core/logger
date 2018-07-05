"""Bitcoin, ethereum, stellar units handling."""
# number of decimals after decimal point in stellar asset
DEC = 7
ETH_DECIMALS = 18
BTC_DECIMALS = 8
STELLAR_DECIMALS = 7
DECIMAL_POINT = '.'


def _divisible_to_indivisible(amount, decimals, numeric_representation=False):
    """
    Convert amount of some currency from divisible units to indivisible.
    :param str or int amount: Amount of units to be converted
    :param int decimals: Number of decimals in convertible currency
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return int or str: amount of indivisible units
    """
    if not isinstance(amount, str) and not (isinstance(amount, int) and not isinstance(amount, bool)):
        raise TypeError('Only string and integer allowed for conversions')

    amount = str(amount)
    if DECIMAL_POINT in amount:
        integer_part, fractional_part = amount.split(DECIMAL_POINT)
        fractional_part = fractional_part[:decimals]
    else:
        integer_part, fractional_part = amount, '0' * decimals

    if integer_part != '0':
        amount = "{0}{1:<0{decimals}}".format(integer_part, fractional_part, decimals=decimals)
    else:
        striped = fractional_part.lstrip('0')
        leading_zeros_amount = len(fractional_part) - len(striped)
        trailing_zeros_amount = decimals - leading_zeros_amount - len(striped)
        amount = "{0}{1}".format(striped, '0' * trailing_zeros_amount)

    amount = amount or '0'
    if numeric_representation:
        amount = int(amount)
    return amount


def stroops_to_units(amount, numeric_representation=False):
    """
    Convert amount presented in stroops to units.
    :param str or int amount: Amount of stroops to be converted
    :param numeric_representation: If true, result will be returned as float number, otherwise - string
    """
    if not isinstance(amount, str) and not (isinstance(amount, int) and not isinstance(amount, bool)):
        raise TypeError('Only string and integer allowed for conversions')

    amount = "{amount:0>{decimals}}".format(amount=amount, decimals=DEC)
    amount = "0.{}".format(amount) if len(amount) == DEC else "{}.{}".format(amount[:-DEC], amount[-DEC:])

    if numeric_representation:
        amount = float(amount)
    return amount


def units_to_stroops(amount, numeric_representation=False):
    """
    Convert stellar units to stroops.
    :param str or int amount: Amount of units to be converted
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return str or int: Amount of stroops
    """
    return _divisible_to_indivisible(amount, STELLAR_DECIMALS, numeric_representation)


def eth_to_wei(amount, numeric_representation=False):
    """
    Convert ethereum to wei
    :param str or int amount: Amount of ethereum to be converted
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return str or int: Amount of wei
    """
    return _divisible_to_indivisible(amount, ETH_DECIMALS, numeric_representation)


def btc_to_satoshi(amount, numeric_representation=False):
    """
    Convert bitcoin to satoshi
    :param amount: Amount of bitcoin to be converted
    :param numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return str or int: Amount of satoshi
    """
    return _divisible_to_indivisible(amount, BTC_DECIMALS, numeric_representation)
