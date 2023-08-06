import re

from django.core.exceptions import ValidationError
from django.db import models

from glitter.assets.fields import AssetForeignKey
from glitter.blocks.video.validators import VIMEO_URL_RE, YOUTUBE_URL_RE
from glitter.models import BaseBlock


class DioceseCarousel(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class DioceseCarouselSlide(models.Model):
    carousel = models.ForeignKey(DioceseCarousel, related_name='carousel_images')
    title = models.CharField(max_length=100)
    subtitle = models.TextField(blank=True)
    link = models.URLField(blank=True)
    is_video = models.BooleanField(default=False, help_text='Check if this slide links to a video')
    html = models.TextField(editable=False)
    image = AssetForeignKey(
        'glitter_assets.Image',
        on_delete=models.PROTECT,
        help_text='If this slide is a video, use an image as a preview /still'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title

    def clean(self):
        if self.link and self.is_video:
            valid_video = (
                re.match(YOUTUBE_URL_RE, self.link) is None and
                re.match(VIMEO_URL_RE, self.link) is None
            )
            if valid_video:
                raise ValidationError(
                    'If "Is video" is checked, please add a complete YouTube or Vimeo URL',
                )

    def get_embed_url(self):
        """ If is video is checked get correct embed url for Youtube or Vimeo. """
        if self.link:
            embed_url = None
            youtube_embed_url = 'https://www.youtube.com/embed/{}'
            vimeo_embed_url = 'https://player.vimeo.com/video/{}'

            # Get video ID from url.
            if re.match(YOUTUBE_URL_RE, self.link):
                embed_url = youtube_embed_url.format(re.match(YOUTUBE_URL_RE, self.link).group(2))
            if re.match(VIMEO_URL_RE, self.link):
                embed_url = vimeo_embed_url.format(re.match(VIMEO_URL_RE, self.link).group(3))
            return embed_url

    def save(self, *args, **kwargs):
        """ Set html field with correct iframe. """
        if self.is_video and self.link:
            self.html = '<iframe src="{}?rel=0" frameborder="0" allowfullscreen></iframe>'.format(
                self.get_embed_url()
            )
        return super().save(*args, **kwargs)


class DioceseCarouselBlock(BaseBlock):
    FAST = 3000
    NORMAL = 5000
    MEDIUM = 7000
    SLOW = 10000
    INTERVAL_CHOICES = (
        (FAST, '4 Seconds'),
        (NORMAL, '5 Seconds'),
        (MEDIUM, '7 Seconds'),
        (SLOW, '10 Seconds'),
    )
    POSITION_CHOICES = (
        ('top', 'Top'),
        ('right', 'Right'),
        ('bottom', 'Bottom'),
        ('left', 'Left'),
    )
    TRANSITION_CHOICES = (
        ('fade', 'Fade'),
        ('slide', 'Slide'),
    )
    ASPECT_CHOICES = (
        ('fluid', 'Fluid'),
        ('wide', '16x9'),
        ('square', 'Square'),
        ('three2', '3x2'),
    )

    carousel = models.ForeignKey(DioceseCarousel, on_delete=models.PROTECT)
    aspect_ratio = models.CharField(
        max_length=6, default='fluid', choices=ASPECT_CHOICES
    )
    navigation_panel_position = models.CharField(
        max_length=6, default='right', choices=POSITION_CHOICES
    )
    transition_style = models.CharField(max_length=5, default='slide', choices=TRANSITION_CHOICES)
    interval = models.PositiveIntegerField(default=NORMAL, choices=INTERVAL_CHOICES)
    auto_play = models.BooleanField(
        default=True, help_text='If unchecked interval will have no effect'
    )
    display_navigation = models.BooleanField(
        default=True, help_text='If checked slide position will have no effect'
    )

    class Meta:
        verbose_name = 'Digital Diocese Carousel'
