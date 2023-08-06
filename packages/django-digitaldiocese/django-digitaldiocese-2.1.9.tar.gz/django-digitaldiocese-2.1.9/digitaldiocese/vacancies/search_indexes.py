# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Vacancy


class VacancyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Vacancy

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related().filter(
            published=True
        ).exclude(
            current_version=None
        )
