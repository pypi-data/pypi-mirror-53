# -*- coding: utf-8 -*-

from django.contrib import admin

from adminsortable.admin import SortableAdmin

from .models import HeaderLink


@admin.register(HeaderLink)
class HeaderLinkAdmin(SortableAdmin):
    list_display = ('title', 'url',)
    fieldsets = (
        (
            'Header link', {
                'fields': ('title', 'url',)
            }
        ),
    )
