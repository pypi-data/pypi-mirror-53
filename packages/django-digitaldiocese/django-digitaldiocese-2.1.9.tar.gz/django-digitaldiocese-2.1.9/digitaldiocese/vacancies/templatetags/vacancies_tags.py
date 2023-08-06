# -*- coding: utf-8 -*-

from django import template

from ..models import Vacancy

register = template.Library()


@register.assignment_tag
def get_latest_vacancies(count=5, category=None):
    vacancy_list = Vacancy.display.active()

    # Optional filter by category
    if category is not None:
        vacancy_list = vacancy_list.filter(category__slug=category)

    return vacancy_list[:count]
