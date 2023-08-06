# -*- coding: utf-8 -*-

from django.contrib.gis.measure import D
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from glitter.mixins import GlitterDetailMixin
from simplejson import JSONEncoderForHTML

from digitaldiocese.search.forms import SearchForm

from .forms import PostcodeForm
from .models import Archdeaconry, Benefice, Church, Deanery, Parish, Person
from .utils import place_geojson


class ACNYMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ACNYMixin, self).get_context_data(**kwargs)
        context['deanery_list'] = Deanery.objects.filter(published=True)
        return context


class BaseChurchListView(ACNYMixin, ListView):
    queryset = Church.objects.select_related().all()

    def get_context_data(self, **kwargs):
        context = super(BaseChurchListView, self).get_context_data(**kwargs)

        geojson_kwargs = {
            'object_list': context['object_list'],
        }

        # Results could be paginated
        page_obj = context.get('page_obj')

        if page_obj is not None:
            geojson_kwargs['start'] = page_obj.start_index()
            context['start_index'] = page_obj.start_index()
        else:
            context['start_index'] = 1

        context['map_json'] = JSONEncoderForHTML().encode(place_geojson(**geojson_kwargs))

        context['search_form'] = SearchForm(self.request.GET or None)

        return context


class ChurchListView(BaseChurchListView):
    paginate_by = 20


class ArchdeaconryView(BaseChurchListView):

    def get_queryset(self):
        qs = super(ArchdeaconryView, self).get_queryset()
        self.archdeaconry = get_object_or_404(Archdeaconry, id=self.kwargs['archdeaconry_id'])
        return qs.filter(archdeaconry=self.archdeaconry)

    def get_context_data(self, **kwargs):
        context = super(ArchdeaconryView, self).get_context_data(**kwargs)
        context['archdeaconry'] = self.archdeaconry
        return context


class BeneficeView(BaseChurchListView):

    def get_queryset(self):
        qs = super(BeneficeView, self).get_queryset()
        self.benefice = get_object_or_404(Benefice, id=self.kwargs['benefice_id'])
        return qs.filter(benefice=self.benefice)

    def get_context_data(self, **kwargs):
        context = super(BeneficeView, self).get_context_data(**kwargs)
        context['benefice'] = self.benefice
        return context


class ParishView(BaseChurchListView):

    def get_queryset(self):
        qs = super(ParishView, self).get_queryset()
        self.parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])
        return qs.filter(parish=self.parish)

    def get_context_data(self, **kwargs):
        context = super(ParishView, self).get_context_data(**kwargs)
        context['parish'] = self.parish
        return context


class DeaneryView(BaseChurchListView):

    def get_queryset(self):
        qs = super(DeaneryView, self).get_queryset()
        self.deanery = get_object_or_404(Deanery, id=self.kwargs['deanery_id'])
        return qs.filter(deanery=self.deanery)

    def get_context_data(self, **kwargs):
        context = super(DeaneryView, self).get_context_data(**kwargs)
        context['deanery'] = self.deanery
        return context


class ChurchDetailView(ACNYMixin, GlitterDetailMixin, DetailView):
    model = Church
    slug_field = 'id'
    slug_url_kwarg = 'church_id'

    def get_context_data(self, **kwargs):
        context = super(ChurchDetailView, self).get_context_data(**kwargs)

        # Only add a map if we have a pin
        if self.object.location:
            church_qs = self.model.objects.filter(id=self.object.id)
            context['map_json'] = JSONEncoderForHTML().encode(place_geojson(church_qs))
        else:
            # Kick out some valid JSON to help in the frontend, even if there's no results.
            context['map_json'] = JSONEncoderForHTML().encode({
                'type': 'FeatureCollection',
                'features': [],
            })

        return context


class PersonListView(ACNYMixin, ListView):
    queryset = Person.objects.select_related().all()
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class PersonDetailView(DetailView):
    model = Person
    slug_field = 'id'
    slug_url_kwarg = 'person_id'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        return context


class PostcodeSearchView(ACNYMixin, ListView):
    queryset = Church.objects.select_related().exclude(location=None)
    template_name = 'digitaldiocese_acny/postcode_search.html'
    search_results = 10
    search_radius = D(mi=10)

    def get(self, request, *args, **kwargs):
        self.location = self.get_location()
        return super(PostcodeSearchView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(PostcodeSearchView, self).get_queryset()

        # Don't show a map without any search parameters
        if self.location is None:
            return qs.none()

        return qs.filter(location__distance_lte=(self.location, self.search_radius)).distance(
            self.location, field_name='location').order_by('distance')[:self.search_results]

    def get_location(self):
        self.form = PostcodeForm(self.request.GET or None)

        if self.form.is_valid():
            return self.form.cleaned_data['q'].location
        else:
            return None

        return None

    def get_context_data(self, **kwargs):
        context = super(PostcodeSearchView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET or None)
        context['location'] = self.location
        context['map_json'] = JSONEncoderForHTML().encode(
            place_geojson(self.object_list))
        context['start_index'] = 1
        return context
