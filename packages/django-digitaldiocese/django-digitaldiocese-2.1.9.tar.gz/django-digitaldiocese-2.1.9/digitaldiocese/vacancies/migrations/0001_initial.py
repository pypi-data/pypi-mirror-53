# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_assets', '0001_initial'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('document', models.FileField(blank=True, upload_to='vacancies/vacancy/%Y/%m')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='LatestVacanciesBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('category', models.ForeignKey(blank=True, to='digitaldiocese_vacancies.Category', null=True)),
                ('content_block', models.ForeignKey(to='glitter.ContentBlock', null=True, editable=False)),
            ],
            options={
                'verbose_name': 'latest vacancies',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('published', models.BooleanField(db_index=True, default=True)),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('summary', models.TextField()),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.URLField(blank=True)),
                ('deadline', models.DateTimeField(db_index=True, blank=True, null=True)),
                ('interview_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='digitaldiocese_vacancies.Category')),
                ('current_version', models.ForeignKey(blank=True, to='glitter.Version', null=True, editable=False)),
                ('image', glitter.assets.fields.AssetForeignKey(blank=True, to='glitter_assets.Image', null=True)),
            ],
            options={
                'verbose_name_plural': 'vacancies',
                'default_permissions': ('add', 'change', 'delete', 'edit', 'publish'),
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='vacancy',
            field=models.ForeignKey(to='digitaldiocese_vacancies.Vacancy'),
        ),
    ]
