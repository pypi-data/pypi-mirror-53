# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0004_legacy_acny_id_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChurchDataLinker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('acny_church_id', models.PositiveIntegerField(null=True, blank=True, db_index=True)),
                ('myd_church_id', models.PositiveIntegerField(null=True, blank=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParishDataLinker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('acny_parish_id', models.PositiveIntegerField(null=True, blank=True, unique=True, db_index=True)),
                ('myd_parish_id', models.PositiveIntegerField(null=True, blank=True, unique=True, db_index=True)),
                ('parish', models.OneToOneField(to='digitaldiocese_acny.Parish', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VenueDataLinker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('acny_venue_id', models.PositiveIntegerField(null=True, blank=True, unique=True, db_index=True)),
                ('church', models.OneToOneField(to='digitaldiocese_acny.Church', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='churchdatalinker',
            name='venue_data_linker',
            field=models.ForeignKey(to='datawrangler.VenueDataLinker'),
        ),
    ]
