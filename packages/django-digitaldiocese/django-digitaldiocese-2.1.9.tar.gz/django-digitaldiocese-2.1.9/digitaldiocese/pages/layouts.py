# -*- coding: utf-8 -*-

from glitter import columns, templates
from glitter.layouts import PageLayout


@templates.attach('glitter_pages.Page')
class Home(PageLayout):
    billboard_top = columns.Column(width=1280)
    header = columns.Column(width=960)
    content = columns.Column(width=640)
    aside = columns.Column(width=320)
    footer = columns.Column(width=960)
    billboard_bottom = columns.Column(width=1280)


@templates.attach('glitter_pages.Page')
class Default(PageLayout):
    billboard_top = columns.Column(width=1280)
    header = columns.Column(width=960)
    content = columns.Column(width=640)
    half_left = columns.Column(width=320)
    half_right = columns.Column(width=320)
    footer = columns.Column(width=960)
    content_2 = columns.Column(width=640)
    billboard_bottom = columns.Column(width=1280)


@templates.attach('glitter_pages.Page')
class Landing(PageLayout):
    billboard_top = columns.Column(width=1280)
    header = columns.Column(width=960)
    content = columns.Column(width=640)
    half_left = columns.Column(width=320)
    half_right = columns.Column(width=320)
    third_left = columns.Column(width=320)
    third_middle = columns.Column(width=320)
    third_right = columns.Column(width=320)
    footer = columns.Column(width=960)
    billboard_bottom = columns.Column(width=1280)


@templates.attach('glitter_news.Post')
class NewsPost(PageLayout):
    content = columns.Column('Main content', width=960)

    class Meta:
        template = 'glitter_news/post_detail.html'


@templates.attach('glitter_news.Post')
class NewsPostWithoutImage(PageLayout):
    content = columns.Column('Main content', width=960)

    class Meta:
        verbose_name = 'News Post (without image)'
        template = 'glitter_news/post_detail_without_image.html'


@templates.attach('glitter_events.Event')
class Event(PageLayout):
    content = columns.Column('Main content', width=960)

    class Meta:
        template = 'glitter_events/event_detail.html'


@templates.attach('glitter_events.Event')
class EventWithoutImage(PageLayout):
    content = columns.Column('Main content', width=960)

    class Meta:
        verbose_name = 'Event (without image)'
        template = 'glitter_events/event_detail_without_image.html'


@templates.attach('glitter_documents.Document')
class Document(PageLayout):
    content = columns.Column('Main content', width=960)

    class Meta:
        template = 'glitter_documents/document_detail.html'
