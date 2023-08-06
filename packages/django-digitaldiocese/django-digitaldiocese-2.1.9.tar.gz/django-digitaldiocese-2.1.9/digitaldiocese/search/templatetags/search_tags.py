# -*- coding: utf-8 -*-

from django import template
from django.utils import six

register = template.Library()


@register.simple_tag
def update_qs(request_get, **kwargs):
    querydict = request_get.copy()

    for k, v in six.iteritems(kwargs):
        querydict[k] = v

    return querydict.urlencode().replace('&', '&amp;')


@register.filter
def result_template(obj):
    return 'search/result/%s_%s.html' % (obj.app_label, obj.model_name)
