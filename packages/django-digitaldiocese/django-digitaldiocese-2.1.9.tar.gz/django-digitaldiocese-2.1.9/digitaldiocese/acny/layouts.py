# -*- coding: utf-8 -*-

from glitter import columns, templates
from glitter.layouts import PageLayout


@templates.attach('digitaldiocese_acny.Church')
class ACNYChurch(PageLayout):
    content = columns.Column(width=640)
