"""Bitcoin, ethereum, stellar units handling."""
# number of decimals after decimal point in stellar asset
ETH_DECIMALS = 18
BTC_DECIMALS = 8
STELLAR_DECIMALS = 7
DECIMAL_POINT = '.'


def divisible_to_indivisible(amount, decimals):
    """
    Convert amount of some currency from divisible units to indivisible.
    :param str or int amount: Amount of units to be converted
    :param int decimals: Number of decimals in convertible currency
    :return int: Amount of indivisible units
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
    return int(amount)


def indivisible_to_divisible(amount, decimals):
    """
    Convert amount of some currency from indivisible units to divisible
    :param str or int amount: Amount of units to be converted
    :param int decimals: Number of decimals in convertible currency
    :return str: Amount of divisible units
    """
    if not isinstance(amount, str) and not (isinstance(amount, int) and not isinstance(amount, bool)):
        raise TypeError('Only string and integer allowed for conversions')

    amount = str(amount)
    amount = "{}.{}".format(amount[:-decimals], amount[-decimals:]) if len(amount) > decimals else \
        "0.{amount:0>{decimals}}".format(amount=amount, decimals=decimals)
    integer_part, fractional_part = amount.split('.')
    striped = fractional_part.rstrip('0')
    amount = "{}.{}".format(integer_part, striped or '0')

    return amount


def stroops_to_units(amount):
    """
    Convert amount presented in stroops to units.
    :param str or int amount: Amount of stroops to be converted
    :param numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str: Amount of stellar units
    """
    return indivisible_to_divisible(amount, STELLAR_DECIMALS)


def units_to_stroops(amount):
    """
    Convert stellar units to stroops.
    :param str or int amount: Amount of units to be converted
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return int: Amount of stroops
    """
    return divisible_to_indivisible(amount, STELLAR_DECIMALS)


def wei_to_eth(amount):
    """
    Convert wei to ethereum
    :param str or int amount: Amount of wei to be converted
    :param bool numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str: Amount of ethereum
    """
    return indivisible_to_divisible(amount, ETH_DECIMALS)


def eth_to_wei(amount):
    """
    Convert ethereum to wei
    :param str or int amount: Amount of ethereum to be converted
    :param bool numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return int: Amount of wei
    """
    return divisible_to_indivisible(amount, ETH_DECIMALS)


def satoshi_to_btc(amount):
    """
    Convert satoshi to bitcoin
    :param str or int amount: Amount of bitcoin to be converted
    :param bool numeric_representation: If true, result will be returned as float number, otherwise - string
    :return str: Amount of bitcoin
    """
    return indivisible_to_divisible(amount, BTC_DECIMALS)


def btc_to_satoshi(amount):
    """
    Convert bitcoin to satoshi
    :param amount: Amount of bitcoin to be converted
    :param numeric_representation: If true, result will be returned as integer number, otherwise - string
    :return int: Amount of satoshi
    """
    return divisible_to_indivisible(amount, BTC_DECIMALS)
