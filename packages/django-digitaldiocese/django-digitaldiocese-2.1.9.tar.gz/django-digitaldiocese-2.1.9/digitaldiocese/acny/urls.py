from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ChurchListView.as_view(), name='church-list'),
    url(
        r'^archdeaconry/(?P<archdeaconry_id>\d+)/$',
        views.ArchdeaconryView.as_view(),
        name='archdeaconry',
    ),
    url(r'^deanery/(?P<deanery_id>\d+)/$', views.DeaneryView.as_view(), name='deanery'),
    url(r'^parish/(?P<parish_id>\d+)/$', views.ParishView.as_view(), name='parish'),
    url(r'^benefice/(?P<benefice_id>\d+)/$', views.BeneficeView.as_view(), name='benefice'),
    url(r'^church/(?P<church_id>\d+)/$', views.ChurchDetailView.as_view(), name='church-detail'),
    url(r'^search/postcode/$', views.PostcodeSearchView.as_view(), name='postcode-search'),
]

# Only add the people specific URLs if that feature has been enabled
if getattr(settings, 'ENABLE_PEOPLE', False):
    people_urlpatterns = [
        url(r'^directory/$', views.PersonListView.as_view(), name='person-list'),
        url(
            r'^person/(?P<person_id>\d+)/$', views.PersonDetailView.as_view(), name='person-detail'
        ),
    ]
    urlpatterns += people_urlpatterns
