# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Archdeaconry, Benefice, Church, Deanery, Parish, Person


class ChurchIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    place_type = indexes.IntegerField(model_attr='place_type')

    def get_model(self):
        return Church

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related().filter(published=True).exclude(
            current_version=None
        )


class DeaneryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Deanery

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class BeneficeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Benefice

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ParishIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Parish

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ArchdeaconryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Archdeaconry

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
