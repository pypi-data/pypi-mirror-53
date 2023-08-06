from django.contrib import admin

from glitter.pages.admin import PageAdmin as BasePageAdmin
from glitter.pages.models import Page

from groot.admin import GrootAdminMixin


class PageAdmin(GrootAdminMixin, BasePageAdmin):
    groot_permissions = ('edit_page', 'publish_page', 'view_protected_page')


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
