from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from ..sqwyre.models import Novel, Token, Reader
from django_facebook import models
from guardian.admin import GuardedModelAdmin
from django.conf import settings

class NovelAdmin(GuardedModelAdmin):
    list_display = ('title', 'authors',  'pitch',)
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['title']
    search_fields = ['title', 'authors', 'pitch']

admin.site.register(Novel, NovelAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'surl', 'stripe_id', 'creator', 'country_code', 'recipient', 'is_valid', 'is_purchased', 'price')
    list_display_links = ('surl',)
    list_per_page = 50
    ordering = ['created_on', 'stripe_id', 'creator', 'country_code', 'recipient', 'is_valid', 'is_purchased', 'price']
    search_fields = ['creator', 'redeemer', 'country_code', 'stripe_id']

admin.site.register(Token, TokenAdmin)

# Facebook users added to admin: http://stackoverflow.com/a/23302897/295606
class AccountAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'facebook_id')

admin.site.register(models.FacebookCustomUser, AccountAdmin)

# https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#extending-the-existing-user-model

# Define an inline admin descriptor for Reader model
# which acts a bit like a singleton
class ReaderInline(admin.StackedInline):
    model = Reader
    can_delete = False
    verbose_name_plural = 'reader'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ReaderInline, )

# Re-register UserAdmin
admin.site.unregister(models.FacebookCustomUser)
admin.site.register(models.FacebookCustomUser, UserAdmin)