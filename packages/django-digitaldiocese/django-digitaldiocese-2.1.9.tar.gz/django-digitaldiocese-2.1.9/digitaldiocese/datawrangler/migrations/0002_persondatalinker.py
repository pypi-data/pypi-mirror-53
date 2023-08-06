# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0005_people_services_blocks'),
        ('datawrangler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonDataLinker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('myd_person_id', models.PositiveIntegerField(db_index=True, null=True, unique=True, blank=True)),
                ('person', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.SET_NULL,
                                                null=True, to='digitaldiocese_acny.Person')),
            ],
        ),
    ]
