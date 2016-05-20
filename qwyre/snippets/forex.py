from django.conf import settings
from django.core.cache import cache

import urllib2                    # For downloading the currency data
import simplejson as json         # Allows the data to be decoded
# https://github.com/ashokfernandez/PyExchangeRates/blob/master/PyExchangeRates.py

CURRENCY_CHOICE = ("gbp", "usd", "eur", "btc")
BASE_CURRENCY = "gbp"

def get_forex(currency=BASE_CURRENCY):
    # https://openexchangerates.org/quick-start
    full_fx = cache.get('full_forex_key', 'has expired')
    if full_fx == 'has expired':
        # Get the latest currency rates from the API
        latest = urllib2.urlopen(settings.OPEXRATE_API_URL)
        full_fx = json.loads(latest.read())
        cache.set('full_forex_key', full_fx)
    fx = {}
    for c in CURRENCY_CHOICE:
        fx[c] = full_fx['rates'][c.upper()]/full_fx['rates'][currency.upper()]
    return fx