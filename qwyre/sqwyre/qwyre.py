from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings

from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms

from ..wiqi.models import Wiqi, Text, WIQI_TYPE_DICT, DEFAULT_WIQISTACK_TYPE
from ..wiqi.forms import TextForm, WIQI_FORM_TYPE_DICT
# http://stackoverflow.com/a/9383295 for ..module format
from ..snippets import html2text 
from ..snippets.diff_match_patch import diff_match_patch
from ..snippets.forex import get_forex

import markdown2
import math
from decimal import Decimal

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_country(request):
    # Specific to using CloudFlare
    # https://support.cloudflare.com/hc/en-us/articles/205072537-What-are-the-two-letter-country-codes-for-the-Access-Rules-
    return request.META.get('HTTP_CF_IPCOUNTRY', settings.COUNTRY_DEFAULT)

def get_price_object(novel_object, request):
    """
    Return only one price for each country. If the queryset returns > 1, return the default
    price for this novel_object. If there's a complete glitch, that's a human-error clusterfuck.
    """
    # country_code = get_user_country(request)
    # Testing
    country_code = 'US'
    from ..sqwyre.models import GlobalPrice
    price_object = GlobalPrice.query.country_price(country_code, novel_object).all()
    if len(price_object) > 1:
        # Any problem, get the One-True-Price(TM)
        return GlobalPrice.objects.get(novel=novel_object, default=True)
    if price_object:
        return price_object[0]
    return False # In case no price_object associated with novel...

def user_has_purchased(request, novel_object):
    """
    We need to return whether or not the user has purchased a copy of the novel being viewed.
    """
    if request.user.is_authenticated():
        return request.user.has_perm("purchased", novel_object)
    else:
        return False
    
def closeness(a, b):
    """
    Returns measure of equality, in unit of decimal significant figures.
    http://stackoverflow.com/a/564086
    """
    a = float(a)
    b = float(b)
    if a == b:
        return float("infinity")
    difference = abs(a - b)
    avg = (a + b)/2
    return math.log10( avg / difference )

def check_fraud(user, price_object, data_object, data_length):
    """
    Very basic fraud protection / detection.
    Anyone who wants to spend time defrauding me of a few pounds
    is clearly insane and not much I can do about it.
    data_object is the data received from the user
    """
    try:
        check_price = price_object.price * 100
        if data_object.get("selfPurchase", False) == "true" and user.is_authenticated():
            if user.reader.current_price > price_object.price:
                check_price = user.reader.current_price * 100
        received_price = int(data_object["stripePrice"])
        fx = get_forex(price_object.currency).get(data_object["stripeCurrency"].lower(), False)
        if not fx:
            return True
        check_price = check_price * Decimal(str(fx)) * data_length
        if data_length >= price_object.discountvolume:
            check_price = check_price / (1 + Decimal(str(price_object.discountpercent)))
        if closeness(int(check_price), received_price) < 1.8:
            return True
        return False
    except Exception:
        # If anything goes wrong, this throws an exception and returns "fraud".
        return True