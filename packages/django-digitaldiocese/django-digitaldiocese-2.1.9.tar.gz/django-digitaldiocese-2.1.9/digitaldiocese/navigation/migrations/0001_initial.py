# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderLink',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
                ('title', models.CharField(max_length=50, db_index=True)),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
    ]
