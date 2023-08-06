# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from glitter import block_admin
from glitter.admin import GlitterAdminMixin

from . import models


@admin.register(models.Archdeaconry)
class ArchdeaconryAdmin(admin.ModelAdmin):
    fields = ('name', 'id', 'worthers_id', 'worthers_updated', 'published')
    readonly_fields = ('name', 'id')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False


@admin.register(models.Deanery)
class DeaneryAdmin(admin.ModelAdmin):
    fields = ('name', 'id', 'legacy_acny_id', 'worthers_id', 'worthers_updated', 'published')
    readonly_fields = ('name', 'id', 'legacy_acny_id', 'worthers_id')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False


@admin.register(models.Benefice)
class BeneficeAdmin(admin.ModelAdmin):
    fields = ('name', 'id', 'worthers_id', 'worthers_updated', 'published')
    readonly_fields = ('name', 'id')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False


@admin.register(models.Parish)
class ParishAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'legacy_acny_id', 'worthers_id', 'worthers_updated')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False


@admin.register(models.ChurchService)
class ChurchServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Service details', {'fields': ('church', 'name', 'notes', 'r_notes', 'labels')}),
        ('Time', {'fields': ('time', 'duration')}),
        ('Day(s)', {
            'fields': (
                'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            )
        }),
        ('Recurrence', {
            'fields': (
                'every_1st_occ', 'every_2nd_occ', 'every_3rd_occ', 'every_4th_occ',
                'every_5th_occ', 'every_occ',
            )
        }),
    )

    list_display = ('church', 'name', 'time', 'duration', 'sunday', 'monday',
                    'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', )


class ChurchServiceInline(admin.StackedInline):
    model = models.ChurchService

    fieldsets = (
        ('Service details', {'fields': ('name', 'notes', 'r_notes', 'labels')}),
        ('Time', {'fields': ('time', 'duration')}),
        ('Day(s)', {
            'fields': (
                'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            )
        }),
        ('Recurrence', {
            'fields': (
                'every_1st_occ', 'every_2nd_occ', 'every_3rd_occ', 'every_4th_occ',
                'every_5th_occ', 'every_occ',
            )
        }),
    )


@admin.register(models.Church)
class ChurchAdmin(GlitterAdminMixin, OSMGeoAdmin):
    fieldsets = (
        ('Church details', {
            'fields': (
                'id', 'legacy_acny_id', 'worthers_id', 'worthers_updated', 'name', 'parish',
                'benefice', 'deanery', 'archdeaconry', 'acny_url', 'website',
            )
        }),
        ('More information', {
            'fields': ('description', 'patron', 'charity_number', 'built', 'architect', )
        }),
        ('Address', {
            'fields': ('road', 'town', 'county', 'postcode', 'location')
        }),
        ('Local details', {
            'fields': ('image', 'phone_number', 'email')
        }),
    )
    readonly_fields = ('id', 'legacy_acny_id', 'name', 'parish', 'deanery', 'archdeaconry',
                       'acny_url', 'website', 'road', 'town', 'county', 'postcode', )
    modifiable = False
    list_display = ('id', 'legacy_acny_id', 'name', 'place_type', 'deanery')
    list_filter = ('place_type', 'deanery',)
    search_fields = ('name', 'legacy_acny_id', 'worthers_id')
    inlines = (ChurchServiceInline, )
    openlayers_url = 'https://openlayers.org/api/2.13/OpenLayers.js'

    def has_add_permission(self, request):
        return False


class PersonAddressInline(admin.StackedInline):
    model = models.PersonAddress


class PersonEmailInline(admin.StackedInline):
    model = models.PersonEmail


class PersonPhoneInline(admin.StackedInline):
    model = models.PersonPhone


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'forenames', 'mailing_name')
    inlines = (PersonEmailInline, PersonPhoneInline, PersonAddressInline, )
    search_fields = ('surname', 'preferred_name', 'mailing_name', 'myd_person_id', )


@admin.register(models.ChurchRole)
class ChurchRoleAdmin(admin.ModelAdmin):
    list_display = ('church', 'person', 'role_name', )
    search_fields = ('role_name', 'myd_tjppid', 'worthers_id', )


@admin.register(models.BeneficeRole)
class BeneficeRoleAdmin(admin.ModelAdmin):
    list_display = ('benefice', 'person', 'role_name', )
    search_fields = ('role_name', 'worthers_id', )


@admin.register(models.ChurchServiceLabel)
class ChurchServiceLabel(admin.ModelAdmin):
    pass


block_admin.site.register(models.PostcodeSearchBlock)
block_admin.site.register_block(models.PostcodeSearchBlock, 'App Blocks')

block_admin.site.register(models.PersonBlock)
block_admin.site.register_block(models.PersonBlock, 'App Blocks')

block_admin.site.register(models.ChurchBlock)
block_admin.site.register_block(models.ChurchBlock, 'App Blocks')

block_admin.site.register(models.RoleBlock)
block_admin.site.register_block(models.RoleBlock, 'App Blocks')
