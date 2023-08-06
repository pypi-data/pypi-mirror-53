# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_assets', '0001_initial'),
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=True, db_index=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('acny_id', models.PositiveIntegerField(unique=True, verbose_name='ACNY ID')),
                ('acny_url', models.URLField(verbose_name='ACNY URL')),
                ('website', models.URLField(blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, null=True)),
                ('road', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=20)),
                ('postcode', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=20, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('current_version', models.ForeignKey(editable=False, null=True, to='glitter.Version', blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'edit', 'publish'),
                'ordering': ('name',),
                'verbose_name_plural': 'churches',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deanery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('acny_id', models.PositiveIntegerField(unique=True, verbose_name='ACNY ID')),
                ('published', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'deaneries',
            },
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('acny_id', models.PositiveIntegerField(unique=True, verbose_name='ACNY ID')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'parishes',
            },
        ),
        migrations.CreateModel(
            name='PostcodeSearchBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_block', models.ForeignKey(editable=False, null=True, to='glitter.ContentBlock')),
            ],
            options={
                'verbose_name': 'postcode search',
            },
        ),
        migrations.AddField(
            model_name='church',
            name='deanery',
            field=models.ForeignKey(to='digitaldiocese_acny.Deanery'),
        ),
        migrations.AddField(
            model_name='church',
            name='image',
            field=glitter.assets.fields.AssetForeignKey(null=True, to='glitter_assets.Image', blank=True),
        ),
        migrations.AddField(
            model_name='church',
            name='parish',
            field=models.ForeignKey(to='digitaldiocese_acny.Parish'),
        ),
    ]
