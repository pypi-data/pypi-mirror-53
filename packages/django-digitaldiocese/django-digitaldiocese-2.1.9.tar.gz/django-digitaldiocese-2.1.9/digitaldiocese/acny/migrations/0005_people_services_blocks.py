# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
        ('digitaldiocese_acny', '0004_legacy_acny_id_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChurchBlock',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
            options={
                'verbose_name': 'church summary',
            },
        ),
        migrations.CreateModel(
            name='ChurchRole',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('role_name', models.CharField(default='', max_length=255, blank=True)),
                ('myd_tjppid', models.PositiveIntegerField(null=True, blank=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChurchService',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('notes', models.TextField(default='', blank=True, verbose_name='event notes')),
                ('r_notes', models.TextField(default='', max_length=255, verbose_name='scheduling notes', blank=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('duration', models.PositiveIntegerField(help_text='minutes', null=True, blank=True)),
                ('sunday', models.BooleanField(default=False)),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
                ('every_1st_occ', models.BooleanField(default=False, verbose_name='every 1st occurence in a month')),
                ('every_2nd_occ', models.BooleanField(default=False, verbose_name='every 2nd occurence in a month')),
                ('every_3rd_occ', models.BooleanField(default=False, verbose_name='every 3rd occurence in a month')),
                ('every_4th_occ', models.BooleanField(default=False, verbose_name='every 4th occurence in a month')),
                ('every_5th_occ', models.BooleanField(default=False, verbose_name='every 5th occurence in a month')),
                ('every_occ', models.BooleanField(default=False, verbose_name='every occurence')),
            ],
        ),
        migrations.CreateModel(
            name='ChurchServiceLabel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(default='', max_length=20, blank=True)),
                ('initials', models.CharField(default='', max_length=10, blank=True)),
                ('forenames', models.CharField(default='', max_length=50, blank=True)),
                ('surname', models.CharField(default='', max_length=50, blank=True)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=1, blank=True)),
                ('preferred_name', models.CharField(default='', max_length=50, blank=True)),
                ('mailing_name', models.CharField(default='', max_length=255, blank=True)),
                ('myd_person_id', models.PositiveIntegerField(null=True, unique=True, blank=True, db_index=True)),
            ],
            options={
                'ordering': ('surname', 'forenames'),
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='PersonAddress',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(default='', max_length=100, blank=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('address_1', models.CharField(default='', max_length=100, blank=True)),
                ('address_2', models.CharField(default='', max_length=100, blank=True)),
                ('address_3', models.CharField(default='', max_length=100, blank=True)),
                ('address_4', models.CharField(default='', max_length=100, blank=True)),
                ('address_5', models.CharField(default='', max_length=100, blank=True)),
                ('town', models.CharField(default='', max_length=150, blank=True)),
                ('postcode', models.CharField(default='', max_length=10, blank=True)),
                ('myd_address_id', models.PositiveIntegerField(null=True, unique=True, blank=True, db_index=True)),
                ('person', models.ForeignKey(related_name='addresses', to='digitaldiocese_acny.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonBlock',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('content_block', models.ForeignKey(editable=False, null=True, to='glitter.ContentBlock')),
                ('person', models.ForeignKey(to='digitaldiocese_acny.Person', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'person summary',
            },
        ),
        migrations.CreateModel(
            name='PersonEmail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=50, blank=True)),
                ('address', models.EmailField(max_length=150)),
                ('myd_address_id', models.PositiveIntegerField(null=True, blank=True, db_index=True)),
                ('person', models.ForeignKey(related_name='emails', to='digitaldiocese_acny.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonPhone',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('phone_type', models.CharField(choices=[('unknown', ''), ('home', 'home'), ('office', 'office'), ('mobile', 'mobile'), ('fax', 'fax')], max_length=10)),
                ('number', models.CharField(max_length=50)),
                ('myd_address_id', models.PositiveIntegerField(null=True, blank=True, db_index=True)),
                ('person', models.ForeignKey(related_name='phone_numbers', to='digitaldiocese_acny.Person')),
            ],
        ),
        migrations.AddField(
            model_name='church',
            name='architect',
            field=models.CharField(default='', max_length=150, blank=True),
        ),
        migrations.AddField(
            model_name='church',
            name='built',
            field=models.CharField(default='', max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='church',
            name='charity_number',
            field=models.CharField(default='', max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='church',
            name='description',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AddField(
            model_name='church',
            name='patron',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='parish',
            name='boundary_data',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='church',
            field=models.ManyToManyField(through='digitaldiocese_acny.ChurchRole', to='digitaldiocese_acny.Church'),
        ),
        migrations.AddField(
            model_name='churchservice',
            name='church',
            field=models.ForeignKey(related_name='services', to='digitaldiocese_acny.Church'),
        ),
        migrations.AddField(
            model_name='churchservice',
            name='labels',
            field=models.ManyToManyField(to='digitaldiocese_acny.ChurchServiceLabel'),
        ),
        migrations.AddField(
            model_name='churchrole',
            name='church',
            field=models.ForeignKey(related_name='people', to='digitaldiocese_acny.Church'),
        ),
        migrations.AddField(
            model_name='churchrole',
            name='person',
            field=models.ForeignKey(related_name='roles', to='digitaldiocese_acny.Person'),
        ),
        migrations.AddField(
            model_name='churchblock',
            name='church',
            field=models.ForeignKey(to='digitaldiocese_acny.Church', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='churchblock',
            name='content_block',
            field=models.ForeignKey(editable=False, null=True, to='glitter.ContentBlock'),
        ),
    ]
