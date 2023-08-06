# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.assets.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_assets', '0001_initial'),
        ('glitter', '0001_initial'),
        ('digitaldiocese_acny', '0011_benefice_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('role_name', models.CharField(blank=True, max_length=255)),
                ('content', models.TextField(blank=True)),
                ('benefice', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='digitaldiocese_acny.Benefice')),
                ('church', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='digitaldiocese_acny.Church')),
                ('content_block', models.ForeignKey(to='glitter.ContentBlock', null=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='beneficerole',
            name='role_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='churchrole',
            name='role_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='image',
            field=glitter.assets.fields.AssetForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, to='glitter_assets.Image'),
        ),
    ]
