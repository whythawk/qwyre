from django.db import models, IntegrityError
from django.core.urlresolvers import reverse
from qwyre.wiqi.models import Wiqi
from qwyre.sqwyre import qwyre as sqwyd

from django.conf import settings
from guardian.shortcuts import assign_perm

from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from jsonfield import JSONField
from decimal import Decimal
import collections
#import shortuuid as shrtn
from django.utils.text import slugify
import re

class Novel(models.Model):
    """
    The novel contains a list of chapters links (wiqis) and all data required for managing
    and distributing sales.
    Since there can be multiple ISBNs and multiple sales channels, it may be necessary to
    spin these fields out into their own models at some point.
    """
    # Core fields
    surl = models.CharField(max_length=30, unique=True, verbose_name="Short URL")
    slug = models.SlugField(unique=True, verbose_name="Slugified URL")
    title = models.CharField(blank=True, max_length=250, verbose_name="Title",
                             help_text="This may be used as a title, section or figure heading.")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                related_name="%(class)s_creator", on_delete=models.CASCADE)
    creator_ip = models.GenericIPAddressField(blank=True, null=True, default="255.255.255.255")
    created_on = models.DateTimeField(auto_now_add=True)
    is_live_from = models.DateTimeField(blank=True, null=True, default=datetime.now, verbose_name="Publish from", 
                                        help_text="Leave blank to publish immediately, otherwise select a future publication date.")
    # Chapters and content
    jsonresponse = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, null=True)
    chapterlist = models.ManyToManyField(Wiqi, related_name="%(class)s_chapterlist", blank=True)
    chapterformat = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, null=True)
    sentinal = models.OneToOneField(Wiqi, related_name="%(class)s_sentinal", blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True)
    # Novel info
    pitch = models.CharField(max_length=503, blank=True, null=True,
                               verbose_name="Elevator Pitch",
                               help_text="You have 503 characters. Sell it to me.")
    summary = models.TextField(blank=True, null=True, verbose_name="Summary",
                               help_text="The back cover of your book.")
    authors = models.CharField(max_length=250, blank=True, null=True,
                               verbose_name="Author names",
                               help_text="Comma-separated list of all authors.")
    authorsort = models.CharField(max_length=250, blank=True, null=True,
                                  verbose_name="Sortable author list",
                                  help_text="Author list by 'surname, name'; for listing.")
    licensing = models.CharField(max_length=50, choices=settings.LICENCE_CHOICE,
                                 default=settings.LICENCE_DEFAULT,
                               verbose_name="Release License", help_text="What form of copyright do you offer?")
    language = models.CharField(max_length=50, blank=True, null=True,
                                verbose_name="Published language",
                                help_text="The language you're writing in.")

    class Meta:
        # http://www.nomadjourney.com/2009/11/splitting-up-django-models/
        app_label = "sqwyre"
        verbose_name_plural = "Novels"
        permissions = (
                       ("can_create", "Can create new novels."),
                       ("can_view", "Can view private novel."),
                       ("can_edit", "Can edit novel."),
                       ("can_publish", "Can change publication status of novel."),
                       ("can_share", "Can share access of novel with others."),
                       ("purchased", "Has purchased the object."),
                       ("borrowed", "Has borrowed the object."),
                       )

    def get_absolute_url(self):
        # http://stackoverflow.com/a/4863504/295606
        return reverse('view_novel', kwargs={'novel_surl': self.surl})

    # def get_prices_url(self):
    #     return reverse('price_novel', kwargs={'novel_surl': self.surl})

    def get_manage_tokens_url(self):
        return reverse('issue_tokens', kwargs={'novel_surl': self.surl})

    def __unicode__(self):
        return self.surl #"Name: %s | Description: %s" % (self.title, self.description)

    @property
    def get_class(self):
        """
        Class name is commonly used and this saves typing
        """
        return self.__class__.__name__.lower()

    def set(self, **kwargs):
        # It's possible to use shrtn for this but, since this is for self-publishing, unless you
        # have a habit of using the same letters again and again, use the shortest possible approach
        # If that doesn't work, return shrtn ...
        #shrtn.set_alphabet(settings.SURL_ALPHABET)
        # while True:
            # the surl must be unique and the likelihood of clash is low, so try again
            # try:
            #     self.surl = shrtn.ShortUUID().random(length=settings.SURL_LENGTH)
            #     self.save()
            # except IntegrityError:
            #     continue
            # else:
            #     break
        # From Stackoverflow: http://stackoverflow.com/a/5775791
        title = BeautifulSoup(kwargs.get("title", "")[:250], "html.parser").get_text().strip()
        self.surl = slugify(title)
        self.slug = slugify(title) # leaves open the future in which we have a surl and slug
        #self.surl = "".join(item[0].lower() for item in re.findall("\w+", title))
        self.save()
        self.title = BeautifulSoup(kwargs.get("title", "")[:250], "html.parser").get_text().strip()
        self.creator = kwargs["creator"]
        self.creator_ip = kwargs.get("creator_ip",None)
        self.licensing = kwargs.get("licensing","(c)")
        self.pitch = BeautifulSoup(kwargs.get("pitch", "")[:503], "html.parser").get_text().strip()
        self.is_live_from = kwargs.get("is_live_from", pytz.UTC.localize(datetime.now()))
        self.save()

    def assign_all_perm(self, usr):
        for perm, perm_text in self._meta.permissions:
            assign_perm(perm, usr, self)

    def refresh_chapters(self, wiqi_object):
        '''
        Process or Refresh all chapters to create the appropriate JSON file;
        :param wiqi_object:
        :return:
        '''
        self.word_count = 0
        self.sentinal = wiqi_object
        # Set the sentinal based on the first wiqi_object
        self.jsonresponse = {'words': self.word_count,
                             'chapters': {},
                             'order': {},
                             'sentinal': {'first': wiqi_object.surl,
                                          'last': wiqi_object.surl
                             }
        }
        count = 1
        while wiqi_object:
            self.word_count += wiqi_object.stack.word_count
            self.jsonresponse['words'] = self.word_count
            self.jsonresponse['chapters'][count] = {'title': wiqi_object.stack.title,
                                                    'subtitle': wiqi_object.stack.subtitle,
                                                    'url': wiqi_object.get_absolute_url(),
                                                    'surl': wiqi_object.surl,
                                                    'price': wiqi_object.price,
                                                    'read_if': wiqi_object.read_if,
                                                    }
            if wiqi_object.next_wiqi:
                next_wiqi = wiqi_object.next_wiqi.surl
            else:
                next_wiqi = None
            if wiqi_object.previous_wiqi:
                previous_wiqi = wiqi_object.previous_wiqi.surl
            else:
                previous_wiqi = None
            self.jsonresponse['order'][wiqi_object.surl] = {'next': next_wiqi,
                                                            'previous': previous_wiqi,
                                                            'i': count,
                                                            }
            self.jsonresponse['sentinal']['last'] = wiqi_object.surl
            wiqi_object = wiqi_object.next_wiqi
            count += 1
        self.save()
        return self

    def add_chapters(self, **kwargs):
        """
        Bulk upload function for receiving new chapters in the form:
            {i: {title: ... , content: ...} ...
        Create new Text chapters and then add them to this book
        """
        if kwargs.get("upload", False):
            self.chapterlist.clear()
            first_wiqi_object = None
            previous_wiqi_object = None
            for i in range(len(kwargs["upload"])):
                if kwargs["upload"][str(i)]: # in case blanks turn up
                    wiqi_object = Wiqi()
                    wiqi_kwargs = kwargs["upload"][str(i)]
                    wiqi_kwargs.update(kwargs["common"])
                    wiqi_object.set(**wiqi_kwargs)
                    wiqi_object.update(**wiqi_kwargs)
                    wiqi_object.assign_all_perm(kwargs["common"]["creator"])
                    if not first_wiqi_object:
                        first_wiqi_object = wiqi_object
                    if previous_wiqi_object:
                        # Assign the previous wiqi to this wiqi
                        wiqi_object.previous_wiqi = previous_wiqi_object
                        wiqi_object.save()
                        previous_wiqi_object.next_wiqi = wiqi_object
                        previous_wiqi_object.save()
                    previous_wiqi_object = wiqi_object
                    # Update the wiqi and novel chapterlist
                    self.chapterlist.add(wiqi_object)
                    wiqi_object.stack.jsonresponse['novelurl'] = self.surl
                    wiqi_object.stack.jsonresponse['noveltitle'] = self.title
                    wiqi_object.stack.save()
            return self.refresh_chapters(first_wiqi_object)
        return self