# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0005_people_services_blocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='personblock',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
