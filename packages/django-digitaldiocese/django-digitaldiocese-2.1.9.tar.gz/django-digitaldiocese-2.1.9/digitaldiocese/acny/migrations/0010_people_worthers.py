# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0009_place_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchrole',
            name='worthers_id',
            field=models.PositiveIntegerField(blank=True, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='churchrole',
            name='worthers_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='worthers_id',
            field=models.PositiveIntegerField(blank=True, unique=True, db_index=True, null=True),
        ),
    ]
