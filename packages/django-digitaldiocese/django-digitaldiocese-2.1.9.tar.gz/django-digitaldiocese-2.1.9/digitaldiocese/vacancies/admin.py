# -*- coding: utf-8 -*-

from django.contrib import admin

from glitter import block_admin
from glitter.admin import GlitterAdminMixin, GlitterPagePublishedFilter

from .models import Attachment, Category, LatestVacanciesBlock, Vacancy


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {
        'slug': ('title',)
    }


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


@admin.register(Vacancy)
class VacancyAdmin(GlitterAdminMixin, admin.ModelAdmin):
    inlines = [AttachmentInline]
    fieldsets = (
        ('Vacancy', {
            'fields': (
                'title', 'category', 'image', 'summary', 'address', 'phone', 'email', 'website',
                'deadline', 'interview_date',
            )
        }),
        ('Advanced options', {
            'fields': ('display_from', 'display_until', 'slug',)
        }),
    )
    date_hierarchy = 'created_at'
    list_display = ('title', 'category', 'deadline', 'interview_date', 'is_published')
    list_filter = (GlitterPagePublishedFilter, 'category',)
    prepopulated_fields = {
        'slug': ('title',)
    }


block_admin.site.register(LatestVacanciesBlock)
block_admin.site.register_block(LatestVacanciesBlock, 'App Blocks')
