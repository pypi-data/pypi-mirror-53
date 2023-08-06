# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0008_auto_20161027_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archdeaconry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('published', models.BooleanField(db_index=True, default=True)),
                ('worthers_id', models.PositiveIntegerField(unique=True, blank=True, null=True)),
                ('worthers_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'archdeaconries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Benefice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('published', models.BooleanField(db_index=True, default=True)),
                ('worthers_id', models.PositiveIntegerField(unique=True, blank=True, null=True)),
                ('worthers_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'benefices',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='church',
            name='place_type',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'church'), (2, 'school')]),
        ),
        migrations.AddField(
            model_name='church',
            name='worthers_id',
            field=models.PositiveIntegerField(unique=True, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='church',
            name='worthers_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deanery',
            name='worthers_id',
            field=models.PositiveIntegerField(unique=True, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deanery',
            name='worthers_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parish',
            name='worthers_id',
            field=models.PositiveIntegerField(unique=True, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='parish',
            name='worthers_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='deanery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='digitaldiocese_acny.Deanery'),
        ),
        migrations.AlterField(
            model_name='church',
            name='parish',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='digitaldiocese_acny.Parish'),
        ),
        migrations.AlterField(
            model_name='church',
            name='phone_number',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='church',
            name='archdeaconry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='digitaldiocese_acny.Archdeaconry'),
        ),
        migrations.AddField(
            model_name='church',
            name='benefice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='digitaldiocese_acny.Benefice'),
        ),
    ]
