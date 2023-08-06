from django.contrib import admin

from .models import ChurchDataLinker, ParishDataLinker, PersonDataLinker, VenueDataLinker


@admin.register(VenueDataLinker)
class VenueDataLinkerAdmin(admin.ModelAdmin):
    list_display = ['church', 'acny_venue_id']
    search_fields = ['acny_venue_id']

    def has_add_permission(self, request):
        return False


@admin.register(ChurchDataLinker)
class ChurchDataLinkerAdmin(admin.ModelAdmin):
    list_display = ['venue_data_linker', 'acny_church_id', 'myd_church_id']
    search_fields = ['acny_church_id', 'myd_church_id']

    def has_add_permission(self, request):
        return False


@admin.register(ParishDataLinker)
class ParishDataLinkerAdmin(admin.ModelAdmin):
    list_display = ['parish', 'acny_parish_id', 'myd_parish_id']
    search_fields = ['acny_parish_id', 'myd_parish_id']

    def has_add_permission(self, request):
        return False


@admin.register(PersonDataLinker)
class PersonDataLinkerAdmin(admin.ModelAdmin):
    list_display = ['person', 'myd_person_id']
    search_fields = ['myd_person_id']

    def has_add_permission(self, request):
        return False
