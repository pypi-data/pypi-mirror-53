# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0014_churchservice_add_date_recurring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
