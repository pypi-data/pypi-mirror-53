# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0003_rename_acny_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='legacy_acny_id',
            field=models.PositiveIntegerField(null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deanery',
            name='legacy_acny_id',
            field=models.PositiveIntegerField(null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='parish',
            name='legacy_acny_id',
            field=models.PositiveIntegerField(null=True, db_index=True, blank=True),
        ),
    ]
