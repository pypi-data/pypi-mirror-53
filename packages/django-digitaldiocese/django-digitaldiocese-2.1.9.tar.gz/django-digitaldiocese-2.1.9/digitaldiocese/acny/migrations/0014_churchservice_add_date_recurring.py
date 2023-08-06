# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0013_rename_church_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchservice',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='churchservice',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
    ]
