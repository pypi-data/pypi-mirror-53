# -*- coding: utf-8 -*-

from django.conf.urls import url

from .forms import SearchForm
from .views import SearchView

urlpatterns = [
    url(
        r'^$',
        SearchView(form_class=SearchForm),
        name='search'
    ),
]
