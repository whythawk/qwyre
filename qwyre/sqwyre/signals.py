#https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners
# http://stackoverflow.com/a/28766343/295606
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..sqwyre.models import Reader

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_has_reader(sender, instance, created, **kwargs):
    if created:
        new_reader = Reader.objects.create(user=instance)
        new_reader.save()