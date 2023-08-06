# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0012_roleblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='churchblock',
            options={'verbose_name': 'Church/School summary'},
        ),
    ]
