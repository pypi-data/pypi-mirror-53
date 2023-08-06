# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0007_role_church_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='built',
            field=models.CharField(max_length=150, blank=True, default=''),
        ),
    ]
