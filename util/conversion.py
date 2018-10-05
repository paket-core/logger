"""Bitcoin, ethereum, stellar units handling. Conversions to and from fiat currencies."""
import requests

import util.logger

# number of decimals after decimal point in currencies
ETH_DECIMALS = 18
BTC_DECIMALS = 8
STELLAR_DECIMALS = 7
DECIMAL_POINT = '.'

# currencies ids on coinmarketcap.com
XLM_ID = 512
ETH_ID = 1027
BTC_ID = 1

LOGGER = util.logger.logging.getLogger('pkt.util.currency_conversions')
MARKET_URL_FORMAT = 'https://api.coinmarketcap.com/v2/ticker/{}/?convert={}'


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
    :return str: Amount of stellar units
    """
    return indivisible_to_divisible(amount, STELLAR_DECIMALS)


def units_to_stroops(amount):
    """
    Convert stellar units to stroops.
    :param str or int amount: Amount of units to be converted
    :return int: Amount of stroops
    """
    return divisible_to_indivisible(amount, STELLAR_DECIMALS)


def wei_to_eth(amount):
    """
    Convert wei to ethereum
    :param str or int amount: Amount of wei to be converted
    :return str: Amount of ethereum
    """
    return indivisible_to_divisible(amount, ETH_DECIMALS)


def eth_to_wei(amount):
    """
    Convert ethereum to wei
    :param str or int amount: Amount of ethereum to be converted
    :return int: Amount of wei
    """
    return divisible_to_indivisible(amount, ETH_DECIMALS)


def satoshi_to_btc(amount):
    """
    Convert satoshi to bitcoin
    :param str or int amount: Amount of bitcoin to be converted
    :return str: Amount of bitcoin
    """
    return indivisible_to_divisible(amount, BTC_DECIMALS)


def btc_to_satoshi(amount):
    """
    Convert bitcoin to satoshi
    :param amount: Amount of bitcoin to be converted
    :return int: Amount of satoshi
    """
    return divisible_to_indivisible(amount, BTC_DECIMALS)


def get_currency_price(id_, convert):
    """
    Get crypto currency price in specified fiat currency.
    Crypto currency specifies as id from coinmarketcap.com
    """
    url = MARKET_URL_FORMAT.format(id_, convert)
    response = requests.get(url)
    price = response.json()['data']['quotes'][convert]['price']
    # we need to cast to string because API returns price as float number
    return str(price)


def currency_to_euro_cents(currency, amount, bul_stroops_price):
    """Convert amount of coins in specified currency to euro cents."""
    assert currency in ['BTC', 'ETH', 'XLM', 'BUL'], 'currency must be BTC, ETH, XLM or BUL'
    if currency == 'BTC':
        eur_price, decimals = get_currency_price(BTC_ID, 'EUR'), BTC_DECIMALS
    elif currency == 'ETH':
        eur_price, decimals = get_currency_price(ETH_ID, 'EUR'), ETH_DECIMALS
    elif currency == 'XLM':
        eur_price, decimals = get_currency_price(XLM_ID, 'EUR'), STELLAR_DECIMALS
    else:
        eur_price, decimals = str(bul_stroops_price / 10 ** STELLAR_DECIMALS * 100), STELLAR_DECIMALS
    price_decimals = len(eur_price.split('.')[1])
    # price in fictitious units (portions of euro cents) by 1 indivisible unit of specified crypto currency
    fictitious_units_price = divisible_to_indivisible(eur_price, price_decimals)
    fictitious_units_amount = fictitious_units_price * amount
    # minus two because initial price was in EUR and we want euro cents
    euro_cents = indivisible_to_divisible(fictitious_units_amount, price_decimals + decimals - 2)
    LOGGER.warning("precision loss: %s converted to %s", euro_cents, round(float(euro_cents)))
    # integer part of result will be amount of euro cents
    return round(float(euro_cents))


def euro_cents_to_xlm_stroops(euro_cents_amount):
    """Convert amount of euro cents to stroops."""
    eur_price = get_currency_price(XLM_ID, 'EUR')
    price_decimals = len(eur_price.split('.')[1])
    fictitious_units_amount = divisible_to_indivisible(euro_cents_amount, STELLAR_DECIMALS + price_decimals)
    fictitious_units_price = divisible_to_indivisible(eur_price, price_decimals + 2)
    stroops = fictitious_units_amount // fictitious_units_price
    LOGGER.warning("precision loss: %s / %s = %s", fictitious_units_amount, fictitious_units_price, stroops)
    return stroops


def euro_cents_to_bul_stroops(euro_cents_amount, bul_stroops_price):
    """Convert amount of euro cents to BUL stroops."""
    return euro_cents_amount * bul_stroops_price
