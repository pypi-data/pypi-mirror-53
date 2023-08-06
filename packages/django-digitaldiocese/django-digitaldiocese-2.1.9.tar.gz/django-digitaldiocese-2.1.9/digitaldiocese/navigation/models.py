# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six.moves import urllib

from adminsortable.models import Sortable


@python_2_unicode_compatible
class HeaderLink(Sortable):
    title = models.CharField(max_length=50, db_index=True)
    url = models.URLField('URL')

    class Meta(Sortable.Meta):
        pass

    def __str__(self):
        return self.title

    @property
    def get_url_path(self):
        """ Get url path. """
        return urllib.parse(self.url).path
