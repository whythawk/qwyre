from django.db import models, IntegrityError
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q

from decimal import Decimal
from qwyre.sqwyre.models import Novel

class CountryCode(models.Model):
    """
    This is purely to have a multichoice list of countries to define regions where particular
    prices hold. E.g. An English-language book can be sold in the US and EU where two entirely
    different pricing regimes hold.
    """
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    
    class Meta:
        app_label = "sqwyre"
        verbose_name_plural = "Countries"

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

class GlobalPriceManager(models.Manager):
    def get_queryset(self):
        return GlobalPriceQuerySet(self.model, using=self._db)
    def country_price(self, country_code, novel_object):
        return self.get_queryset().country_price(country_code, novel_object)

class GlobalPrice(models.Model):
    """
    A novel can be sold in many different markets where pricing may vary as a result of local
    factors, tax, etc.
    """
    #https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey.related_query_name
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE,
                              related_name="price",
                              related_query_name="price",)
    countrylist = models.ManyToManyField(CountryCode, related_name="global_pricing", blank=True)
    currency = models.CharField(max_length=7, choices=settings.CURRENCY_CHOICE,
                                default=settings.CURRENCY_DEFAULT)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    query = GlobalPriceManager()

    class Meta:
        app_label = "sqwyre"
        verbose_name_plural = "Prices"