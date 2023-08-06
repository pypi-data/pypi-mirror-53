# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitaldiocese_acny', '0010_people_worthers'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeneficeRole',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('role_name', models.CharField(max_length=255, blank=True, default='')),
                ('worthers_id', models.PositiveIntegerField(blank=True, null=True)),
                ('worthers_updated', models.DateTimeField(blank=True, null=True)),
                ('benefice', models.ForeignKey(related_name='benefice_people', null=True, blank=True, to='digitaldiocese_acny.Benefice')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='worthers_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='churchrole',
            name='worthers_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beneficerole',
            name='person',
            field=models.ForeignKey(to='digitaldiocese_acny.Person', related_name='benefice_roles'),
        ),
    ]
