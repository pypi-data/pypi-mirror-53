# -*- coding: utf-8 -*-

from django import template

from glitter.pages.models import Page
from mptt.templatetags.mptt_tags import cache_tree_children

register = template.Library()


@register.assignment_tag
def footer_pages():
    page_qs = Page.objects.exclude(level__gt=1)
    return cache_tree_children(page_qs)


@register.filter
def show_nav(pages):
    if pages:
        pages = [x for x in pages if x.show_in_navigation]
    return pages
