# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_vacancies', '0002_attachment_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='display_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='display_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
