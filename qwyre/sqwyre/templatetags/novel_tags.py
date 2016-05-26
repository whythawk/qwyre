from django import template
from django.core.exceptions import ObjectDoesNotExist
#https://docs.python.org/3/library/collections.html#collections.OrderedDict
from collections import OrderedDict as SortedDict

register = template.Library()

@register.filter
def numdict(kwargs):
    """
    A method to handle a list of items in a dict with numeric keys
    :param kwargs:
    """
    dictlist = []
    for i in range(1, len(kwargs)+1):
        dictlist.append(kwargs[str(i)])
    return dictlist

@register.filter
def orderchapters(formset):
    """
    Returns an ordered set of chapters based on the position of the sentinal.
    :param formset:
    :return:
    """
    formsetlist = []
    formsetdict = {}
    sentinal = False
    for form in formset:
        formsetdict[form.instance.surl] = form
        try:
            form.instance.novel_sentinal
            sentinal = form.instance
            formsetlist.append(form)
        except ObjectDoesNotExist:
            pass
    if sentinal:
        while sentinal.next_wiqi:
            sentinal = sentinal.next_wiqi
            formsetlist.append(formsetdict[sentinal.surl])
        return formsetlist
    return formset

@register.filter(name='sort')
def listsort(value):
    if isinstance(value, dict):
        new_dict = SortedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        value = sorted([(int(k), v) for (k, v) in value])
        return value
    else:
        return value
    listsort.is_safe = True
    
@register.filter
def get_item(dictionary, key):
    # http://stackoverflow.com/a/8000091/295606
    return dictionary.get(key)

@register.simple_tag
def can_show_link(is_auth, read_type, can_buy, can_read):
    '''
    Where:
        is_auth = request.user.is_authenticated
        read_type = open, logfree, login, or own
        can_buy = T/F
        can_read = purchased, borrowed, False
    Based on these, return whether or not to show link.
    Show if:
        "open" or "logfree"
        can_buy and login
        can_buy and is_auth
            
    '''
    if ((read_type in ["open", "logfree"]) or
        (can_buy and read_type == "login") or
        (can_buy and is_auth) or
        (is_auth and can_read)):
        return True
    return False