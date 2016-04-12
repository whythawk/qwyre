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
    return request.META.get('HTTP_CF_IPCOUNTRY', 'GB')

def get_price_object(novel_object, country_code):
    """
    Return only one price. If the queryset returns > 1, return the default price for
    this novel_object. If there's a complete glitch, that's a human-error clusterfuck.
    """
    pricelist = GlobalPrice.query.country_price(country_code, novel_object).all()
    if len(pricelist) > 1:
        pricelist = GlobalPrice.query.country_price(settings.COUNTRY_DEFAULT, novel_object).all()
    return pricelist[0]

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

def check_fraud(user, novel_object, data_object, data_length):
    """
    Very basic fraud protection / detection.
    Anyone who wants to spend time defrauding me of a few pounds
    is clearly insane and not much I can do about it.
    data_object is the data received from the user
    """
    try:
        check_price = novel_object.get_price_object.price * 100
        if data_object.get("selfPurchase", False) == "true" and user.is_authenticated():
            if user.reader.current_price > novel_object.get_price_object.price:
                check_price = user.reader.current_price * 100
        received_price = int(data_object["stripePrice"])
        fx = get_forex().get(data_object["stripeCurrency"].lower(), False)
        if not fx:
            return True
        check_price = check_price * Decimal(str(fx)) * data_length
        if data_length >= novel_object.discountvolume:
            check_price = check_price / (1 + Decimal(str(novel_object.discountpercent)))
        if closeness(int(check_price), received_price) < 1.8:
            return True
        return False
    except Exception:
        # If anything goes wrong, this throws an exception and returns "fraud".
        return True