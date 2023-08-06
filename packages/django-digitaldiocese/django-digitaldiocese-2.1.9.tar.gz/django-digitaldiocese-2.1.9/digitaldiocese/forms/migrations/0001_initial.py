# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
        ('glitter_pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddressFormBlock',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('recipient', models.EmailField(max_length=254)),
                ('content_block', models.ForeignKey(to='glitter.ContentBlock', editable=False, null=True)),
                ('success_page', mptt.fields.TreeForeignKey(null=True, to='glitter_pages.Page', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'email address submission',
            },
        ),
    ]
