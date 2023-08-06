# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0015_title_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='architect',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='church',
            name='built',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='church',
            name='county',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='church',
            name='postcode',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='church',
            name='road',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='church',
            name='town',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='person',
            name='forenames',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='person',
            name='initials',
            field=models.CharField(blank=True, max_length=50, default=''),
        ),
        migrations.AlterField(
            model_name='person',
            name='preferred_name',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='address_1',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='address_2',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='address_3',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='address_4',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='address_5',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='postcode',
            field=models.CharField(blank=True, max_length=50, default=''),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='town',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
    ]
