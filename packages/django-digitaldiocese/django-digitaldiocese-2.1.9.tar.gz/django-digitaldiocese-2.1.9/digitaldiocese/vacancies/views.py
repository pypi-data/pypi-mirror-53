from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from glitter.mixins import GlitterDetailMixin

from .mixins import VacancyDetailMixin, VacancyListMixin
from .models import Category


class VacancyListView(VacancyListMixin, ListView):
    paginate_by = 10


class VacancyDetailView(VacancyDetailMixin, GlitterDetailMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(VacancyDetailView, self).get_context_data(**kwargs)
        context['current_category'] = self.object.category
        return context


class CategoryVacancyListView(VacancyListMixin, ListView):
    template_name_suffix = '_category_list'
    paginate_by = 10

    def get_queryset(self):
        qs = super(CategoryVacancyListView, self).get_queryset()
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return qs.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryVacancyListView, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        context['categories'] = Category.objects.all()
        return context
