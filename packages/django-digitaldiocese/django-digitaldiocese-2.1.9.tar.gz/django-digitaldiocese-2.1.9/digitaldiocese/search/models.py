from django.db import models

from glitter.models import BaseBlock


class SearchBlock(BaseBlock):
    """
    A generic search block, allowing users to search for pre-defined types of things.
    """

    title = models.CharField(max_length=255, blank=True, default='Search')
    content_type = models.CharField(max_length=100, blank=True)
    placeholder_text = models.CharField(max_length=50, default='search')
    button_text = models.CharField(max_length=50, default='Search')
