# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from glitter.assets.fields import AssetForeignKey
from glitter.mixins import GlitterMixin
from glitter.models import BaseBlock

from .managers import VacancyManager


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('digitaldiocese-vacancies:category-list', args=(self.slug,))


@python_2_unicode_compatible
class Vacancy(GlitterMixin):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category)
    image = AssetForeignKey('glitter_assets.Image', null=True, blank=True)
    summary = models.TextField()
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    deadline = models.DateTimeField(blank=True, null=True, db_index=True)
    interview_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_from = models.DateTimeField(null=True, blank=True)
    display_until = models.DateTimeField(null=True, blank=True)

    display = VacancyManager()

    class Meta(GlitterMixin.Meta):
        verbose_name_plural = 'vacancies'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('digitaldiocese-vacancies:detail', args=(self.slug,))


class Attachment(models.Model):
    vacancy = models.ForeignKey(Vacancy)
    title = models.CharField(max_length=32)
    document = models.FileField(upload_to='vacancies/vacancy/%Y/%m')


class LatestVacanciesBlock(BaseBlock):
    category = models.ForeignKey(Category, null=True, blank=True)

    class Meta:
        verbose_name = 'latest vacancies'
