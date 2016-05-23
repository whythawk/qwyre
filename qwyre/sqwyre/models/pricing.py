from django.db import models, IntegrityError
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.text import slugify

from decimal import Decimal
from datetime import datetime
import pytz
from qwyre.sqwyre.models import Novel

class CountryCodeQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/dev/topics/db/managers/#calling-custom-queryset-methods-from-the-manager
    # http://stackoverflow.com/a/5956422/295606
    def country_list(self, code_list):
        """
        Return a list of countries from a list of ISO codes.
        """
        c_list = Q()
        for code in code_list:
            c_list = c_list | Q(code=code)
        return self.filter(c_list)

class CountryCodeManager(models.Manager):
    def get_queryset(self):
        return CountryCodeQuerySet(self.model, using=self._db)
    def country_list(self, code_list):
        return self.get_queryset().country_list(code_list)

class CountryCode(models.Model):
    """
    This is purely to have a multichoice list of countries to define regions where particular
    prices hold. E.g. An English-language book can be sold in the US and EU where two entirely
    different pricing regimes hold.
    """
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    objects = models.Manager()
    query = CountryCodeManager()
    
    class Meta:
        app_label = "sqwyre"
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

class GlobalPriceQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/dev/topics/db/managers/#calling-custom-queryset-methods-from-the-manager
    def country_price(self, country_code, novel_object):
        """
        Return a single price applying to this country code. If there's a glitch
        return only the CURRENCY_DEFAULT for this novel.
        """
        return self.filter(
            Q(countrylist__code=country_code) &
            Q(novel=novel_object)
            )
    def novel_price(self, novel_object):
        return self.filter(Q(novel=novel_object))
    
class GlobalPriceManager(models.Manager):
    def get_queryset(self):
        return GlobalPriceQuerySet(self.model, using=self._db)
    def country_price(self, country_code, novel_object):
        return self.get_queryset().country_price(country_code, novel_object)
    def novel_price(self, novel_object):
        return self.get_queryset().novel_price(novel_object)

class GlobalPrice(models.Model):
    """
    A novel can be sold in many different markets where pricing may vary as a result of local
    factors, tax, etc.
    """
    #https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey.related_query_name
    region = models.CharField(max_length=50, verbose_name="Region",
                              help_text="Price and region for download.")
    slug = models.SlugField(verbose_name="Slugified URL")
    default = models.BooleanField(default=False)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE,
                              related_name="price",
                              related_query_name="price",)
    countrylist = models.ManyToManyField(CountryCode, related_name="global_pricing", blank=True)
    # Managing sales and distribution
    can_buy = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_live_from = models.DateTimeField(blank=True, null=True, default=datetime.now, verbose_name="Publish from", 
                                        help_text="Leave blank to publish immediately, otherwise select a future publication date.")
    discountvolume = models.IntegerField(default=0)
    discountpercent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    lendnumber = models.IntegerField(default=0)
    lenddays = models.IntegerField(default=0)
    currency = models.CharField(max_length=7, choices=settings.CURRENCY_CHOICE,
                                default=settings.CURRENCY_DEFAULT)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    download_folder = models.CharField(blank=True, max_length=50, verbose_name="Download Folder",
                                       help_text="S3 download folder.")
    # https://docs.djangoproject.com/en/1.9/topics/db/managers/
    objects = models.Manager()
    query = GlobalPriceManager()

    class Meta:
        app_label = "sqwyre"
        verbose_name_plural = "GlobalPrices"

    def set(self, **kwargs):
        """
        This should only be called after a novel has been created.
        Any price object needs the following:
            REGION - name
            COUNTRIES - two-letter ISO codes from COUNTRY_CODES
            PRICE - text format "0.00"
            CURRENCY - from CURRENCY_CHOICE
        For the moment - big danger!!!! - assuming that no overlap between regions
        """
        # Check if exists...
        if not kwargs.get("region", False):
            return False
        # Core Fields
        self.region = kwargs["region"]
        self.slug = slugify(kwargs["region"])
        self.price = kwargs.get("price", "0.00")
        self.novel = kwargs['novel']
        self.currency = kwargs.get("currency", settings.COUNTRY_DEFAULT)
        self.default = kwargs.get("default", False)
        self.is_live_from = kwargs.get("is_live_from", pytz.UTC.localize(datetime.now()))
        # Non-core fields
        self.can_buy = kwargs.get("can_buy", False)
        self.discountvolume = kwargs.get("discountvolume", 0)
        self.discountpercent = kwargs.get("discountpercent", "0.00")
        self.lendnumber = kwargs.get("lendnumber", 0)
        self.lenddays = kwargs.get("lenddays", 0)
        self.download_folder = kwargs.get("download_folder", "")
        self.save()
        countrylist = kwargs.get("countrylist", CountryCode.objects.all())
        self.countrylist.add(*countrylist)
        self.save()
        return self

    @property
    def is_preorder(self):
        return self.is_live_from > pytz.UTC.localize(datetime.now())
    
    @property
    def is_preorder_text(self):
        if self.is_preorder:
            return "Preorder"
        else:
            return "Buy"

    @property
    def was_preorder(self):
        # Quick check if this was ever a preorder ...
        return abs((self.is_live_from - self.novel.created_on).days) > 1
    
    @property
    def currency_verbose(self):
        # http://stackoverflow.com/a/20204400/295606
        return dict(settings.CURRENCY_CHOICE)[self.currency]

    def is_valid_isbn13(self, test_isbn):
        # http://stackoverflow.com/a/1249424
        isbn = re.sub("[^0-9]", "", test_isbn)
        # http://en.wikipedia.org/wiki/International_Standard_Book_Number
        check = (10 - (sum(int(digit) * (3 if idx % 2 else 1) for idx, digit in enumerate(isbn[:12])) % 10)) % 10
        return check == int(isbn[-1])
    
    # def countrylist_names(self):
    #     # http://stackoverflow.com/a/4564449/295606
    #     return ', '.join([a.name for a in self.countrylist.all()])
    # admin_names.short_description = "Admin Names"