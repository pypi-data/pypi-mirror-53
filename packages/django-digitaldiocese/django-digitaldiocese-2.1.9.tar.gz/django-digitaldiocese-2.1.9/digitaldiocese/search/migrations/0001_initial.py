# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(blank=True, default='Search', max_length=255)),
                ('content_type', models.CharField(blank=True, max_length=100)),
                ('placeholder_text', models.CharField(default='search', max_length=50)),
                ('button_text', models.CharField(default='Search', max_length=50)),
                ('content_block', models.ForeignKey(editable=False, null=True, to='glitter.ContentBlock')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
