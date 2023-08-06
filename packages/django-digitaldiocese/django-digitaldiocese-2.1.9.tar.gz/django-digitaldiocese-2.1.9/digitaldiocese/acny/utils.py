import json

from django.contrib.gis.geos import Point
from django.forms import ValidationError

import requests


def place_geojson(object_list, start=1):
    features = []

    for num, obj in enumerate(object_list, start=start):
        if obj.location:
            features.append({
                'type': 'Feature',
                'properties': {
                    'name': obj.name,
                    'number': num,
                    'link': obj.get_absolute_url(),
                },
                'geometry': json.loads(obj.location.json),
            })

    multipoint = object_list.collect()

    if object_list and multipoint:
        features.append({
            'type': 'Feature',
            'properties': {
                'centroid': True,
            },
            'geometry': json.loads(multipoint.centroid.json),
        })

        features.append({
            'type': 'Feature',
            'properties': {
                'envelope': True,
            },
            'geometry': json.loads(multipoint.envelope.json),
        })

    return {
        'type': 'FeatureCollection',
        'features': features,
    }


def get_location(base_url, postcode):
    r = requests.get('%s%s' % (base_url, postcode))

    # Invalid in some way
    if r.status_code != 200:
        raise ValidationError("Can't find a valid location for that postcode")

    mapit_data = r.json()

    try:
        location = Point(mapit_data['wgs84_lon'], mapit_data['wgs84_lat'], srid=4326)
    except KeyError:
        # No location? Shouldn't happen, but just incase
        raise ValidationError("Can't find a valid location for that postcode")

    return location


def get_postcode_location(postcode):
    return get_location('http://greendale.devsoc.org/postcode/', postcode)


def get_partial_postcode_location(postcode):
    return get_location('http://greendale.devsoc.org/postcode/partial/', postcode)
