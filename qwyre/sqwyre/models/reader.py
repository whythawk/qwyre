from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm, get_objects_for_user, remove_perm
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from qwyre.sqwyre.models import Novel
from decimal import Decimal

class Reader(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #settings.AUTH_USER_MODEL is changed
    current_view = models.CharField(max_length=32, blank=True, verbose_name="Current chapter view.")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    optout = models.BooleanField(default=False)

    class Meta:
        # http://www.nomadjourney.com/2009/11/splitting-up-django-models/
        app_label = "qwyre"
        verbose_name_plural = "Readers"

    def take_ownership(self, novel_object, view_perm):
        """
        Assign appropriate permissions to user for access after purchase or being loaned the novel.
        :param kwargs:
        :return:
        """
        for chapter in novel_object.chapterlist.all():
            assign_perm(view_perm, self.user, chapter)
        assign_perm(view_perm, self.user, novel_object)
    
    def current_token(self, purchased=False):
        return self.user.token_redeemer.filter(is_purchased=purchased).order_by('-redeemed_on')[0]

    def deadline(self, token_object=None):
        try:
            if not token_object:
                token_object = self.current_token()
            return token_object.redeemed_on + timedelta(days=token_object.novel.lenddays)
        except:
            return False
        
    def return_borrowed(self, novel_object, token_object):
        """
        Remove all borrowed permissions on the novel
        :param novel_object:
        :return:
        """
        if novel_object.get_class == "text":
            novel_object = novel_object.novel_chapterlist.all()[0]
        remove_perm("borrowed", self.user, novel_object)
        for chapter in novel_object.chapterlist.all():
            remove_perm("borrowed", self.user, chapter)
        token_object.delete()

    def can_read(self, novel_object):
        """
        If novel is owned then True; if novel is borrowed, check if still valid and return status;
        If not valid, removed borrowed permissions;
        :param novel_object:
        :return:
        """
        if self.user.has_perm("purchased", novel_object):
            return "purchased"
        if self.user.has_perm("borrowed", novel_object):
            token_object = self.current_token()
            if self.deadline(token_object) and self.deadline(token_object) > pytz.UTC.localize(datetime.now()):
                return "borrowed"
            else:
                self.return_borrowed(novel_object, token_object)
        return False

    def can_read_terms(self, item):
        """
        Return the text version of the terms of readership for a particular item
        :param kwargs:
        :return:
        """
        if self.user.has_perm("purchased", item):
            return "You own %s." % item.title
        if self.user.has_perm("borrowed", item):
            token_object = self.current_token()
            # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            deadline = self.deadline(token_object).strftime('%d %B %Y')
            return "%s has lent you %s until %s." % (token_object.creator.username, item.title, deadline)
        return "You don't have access to %s." % item.title
