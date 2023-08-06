# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0006_personblock_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churchrole',
            name='church',
            field=models.ForeignKey(related_name='people', blank=True, to='digitaldiocese_acny.Church', null=True),
        ),
    ]
