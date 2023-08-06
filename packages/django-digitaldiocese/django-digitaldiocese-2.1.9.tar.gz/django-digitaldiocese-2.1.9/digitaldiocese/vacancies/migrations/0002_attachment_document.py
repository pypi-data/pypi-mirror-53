# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_vacancies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='document',
            field=models.FileField(upload_to='vacancies/vacancy/%Y/%m'),
        ),
    ]
