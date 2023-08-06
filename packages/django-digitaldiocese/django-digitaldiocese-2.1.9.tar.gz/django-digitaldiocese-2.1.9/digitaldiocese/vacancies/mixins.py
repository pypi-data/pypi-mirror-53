# -*- coding: utf-8 -*-

from .models import Category, Vacancy


class VacancyDetailMixin(object):
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(VacancyDetailMixin, self).get_context_data(**kwargs)
        context['vacancies_categories'] = True
        context['categories'] = Category.objects.all()
        return context


class VacancyListMixin(VacancyDetailMixin):
    def get_queryset(self):
        return self.model.display.active()
