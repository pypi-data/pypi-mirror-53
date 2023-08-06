# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import glitter.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_assets', '0002_image_category_field_optional'),
        ('glitter', '0004_object_id_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='DioceseCarousel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, db_index=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='DioceseCarouselBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('aspect_ratio', models.CharField(max_length=6, choices=[('fluid', 'Fluid'), ('wide', '16x9'), ('square', 'Square'), ('three2', '3x2')], default='fluid')),
                ('navigation_panel_position', models.CharField(max_length=6, choices=[('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left')], default='right')),
                ('transition_style', models.CharField(max_length=5, choices=[('fade', 'Fade'), ('slide', 'Slide')], default='slide')),
                ('interval', models.PositiveIntegerField(choices=[(3000, '4 Seconds'), (5000, '5 Seconds'), (7000, '7 Seconds'), (10000, '10 Seconds')], default=5000)),
                ('auto_play', models.BooleanField(help_text='If unchecked interval will have no effect', default=True)),
                ('display_navigation', models.BooleanField(help_text='If checked slide position will have no effect', default=True)),
                ('carousel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='digitaldiocese_carousel.DioceseCarousel')),
                ('content_block', models.ForeignKey(null=True, editable=False, to='glitter.ContentBlock')),
            ],
            options={
                'verbose_name': 'Digital Diocese Carousel',
            },
        ),
        migrations.CreateModel(
            name='DioceseCarouselSlide',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('is_video', models.BooleanField(help_text='Check if this slide links to a video', default=False)),
                ('html', models.TextField(editable=False)),
                ('carousel', models.ForeignKey(to='digitaldiocese_carousel.DioceseCarousel', related_name='carousel_images')),
                ('image', glitter.assets.fields.AssetForeignKey(help_text='If this slide is a video, use an image as a preview /still', on_delete=django.db.models.deletion.PROTECT, to='glitter_assets.Image')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
