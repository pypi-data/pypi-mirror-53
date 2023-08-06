# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0002_county_length'),
    ]

    operations = [
        migrations.RenameField(
            model_name='church',
            old_name='acny_id',
            new_name='legacy_acny_id',
        ),
        migrations.RenameField(
            model_name='deanery',
            old_name='acny_id',
            new_name='legacy_acny_id',
        ),
        migrations.RenameField(
            model_name='parish',
            old_name='acny_id',
            new_name='legacy_acny_id',
        ),
    ]
