# -*- coding: utf-8 -*-

from .models import HeaderLink


def header_links(request):
    return {
        'header_links': HeaderLink.objects.all(),
    }
