# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps
from django.conf import settings

from haystack.forms import SearchForm as HaystackSearchForm

from digitaldiocese.acny import choices

from .models import SearchBlock


class SearchForm(HaystackSearchForm):
    MODEL_CHOICES = [('', 'Everything'), ]

    MODEL_CHOICES.append(('glitter_pages.Page', 'Pages'))
    if getattr(settings, 'ENABLE_SEARCH_ACNY', True):
        MODEL_CHOICES.append(('digitaldiocese_acny.Archdeaconry', 'Archdeaconries'))
        MODEL_CHOICES.append(('digitaldiocese_acny.Deanery', 'Deaneries'))
        MODEL_CHOICES.append(('digitaldiocese_acny.Benefice', 'Benefices'))
        MODEL_CHOICES.append(('digitaldiocese_acny.Parish', 'Parishes'))
        MODEL_CHOICES.append(('digitaldiocese_acny.Church', 'Churches'))

    if getattr(settings, 'ENABLE_SCHOOLS', False):
        MODEL_CHOICES.append(('digitaldiocese_acny.School', 'Schools'))

    if getattr(settings, 'ENABLE_PEOPLE', False):
        MODEL_CHOICES.append(('digitaldiocese_acny.Person', 'People')),

    MODEL_CHOICES.append(('glitter_news.Post', 'News'))
    MODEL_CHOICES.append(('glitter_events.Event', 'Events'))
    MODEL_CHOICES.append(('glitter_documents.Document', 'Files'))
    MODEL_CHOICES.append(('digitaldiocese_vacancies.Vacancy', 'Vacancies'))
    content_type = forms.ChoiceField(choices=MODEL_CHOICES, required=False)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        # Search query with partial word matching
        qs = self.searchqueryset.filter(text__contains=self.cleaned_data.get('q'))

        # Model filtering
        content_type = self.cleaned_data.get('content_type')

        if content_type:

            if getattr(settings, 'ENABLE_SCHOOLS', False):

                if content_type == 'digitaldiocese_acny.School':
                    content_type = 'digitaldiocese_acny.Church'
                    qs = qs.models(apps.get_model(*content_type.split('.'))).filter(
                        place_type=choices.PLACE_TYPE_SCHOOL
                    )
                    return qs

                elif content_type == 'digitaldiocese_acny.Church':
                    qs = qs.models(apps.get_model(*content_type.split('.'))).filter(
                        place_type=choices.PLACE_TYPE_CHURCH
                    )
                    return qs

            qs = qs.models(apps.get_model(*content_type.split('.')))

        return qs


class SearchBlockAdminForm(forms.ModelForm):
    class Meta:
        model = SearchBlock
        fields = '__all__'
        widgets = {'content_type': forms.Select(choices=SearchForm.MODEL_CHOICES)}
