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
    :return int or str: Amount of indivisible units
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


def _indivisible_to_divisible(amount, decimals, numeric_representation=False):
    """
    Convert amount of some currency from indivisible units to divisible
    :param str or int amount: Amount of units to be converted
    :param int decimals: Number of decimals in convertible currency
    :param bool numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str or float: Amount of divisible units
    """
    if not isinstance(amount, str) and not (isinstance(amount, int) and not isinstance(amount, bool)):
        raise TypeError('Only string and integer allowed for conversions')

    amount = str(amount)
    amount = "{}.{}".format(amount[:-decimals], amount[-decimals:]) if len(amount) > decimals else \
        "0.{amount:0>{decimals}}".format(amount=amount, decimals=decimals)
    integer_part, fractional_part = amount.split('.')
    striped = fractional_part.rstrip('0')
    amount = "{}.{}".format(integer_part, striped or '0')

    if numeric_representation:
        amount = float(amount)
    return amount


def stroops_to_units(amount, numeric_representation=False):
    """
    Convert amount presented in stroops to units.
    :param str or int amount: Amount of stroops to be converted
    :param numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str or float: Amount of stellar units
    """
    return _indivisible_to_divisible(amount, STELLAR_DECIMALS, numeric_representation)


def units_to_stroops(amount, numeric_representation=False):
    """
    Convert stellar units to stroops.
    :param str or int amount: Amount of units to be converted
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return str or int: Amount of stroops
    """
    return _divisible_to_indivisible(amount, STELLAR_DECIMALS, numeric_representation)


def wei_to_eth(amount, numeric_representation=False):
    """
    Convert wei to ethereum
    :param str or int amount: Amount of wei to be converted
    :param bool numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str or float: Amount of ethereum
    """
    return _indivisible_to_divisible(amount, ETH_DECIMALS, numeric_representation)


def eth_to_wei(amount, numeric_representation=False):
    """
    Convert ethereum to wei
    :param str or int amount: Amount of ethereum to be converted
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return str or int: Amount of wei
    """
    return _divisible_to_indivisible(amount, ETH_DECIMALS, numeric_representation)


def satoshi_to_btc(amount, numeric_representation=False):
    """
    Convert satoshi to bitcoin
    :param str or int amount: Amount of bitcoin to be converted
    :param bool numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str or float : Amount of bitcoin
    """
    return _indivisible_to_divisible(amount, BTC_DECIMALS, numeric_representation)


def btc_to_satoshi(amount, numeric_representation=False):
    """
    Convert bitcoin to satoshi
    :param amount: Amount of bitcoin to be converted
    :param numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return str or int: Amount of satoshi
    """
    return _divisible_to_indivisible(amount, BTC_DECIMALS, numeric_representation)
