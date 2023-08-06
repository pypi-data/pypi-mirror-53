import re

from django.forms import ValidationError

from localflavor.gb.forms import GBPostcodeField

from .utils import get_partial_postcode_location, get_postcode_location


class PostcodeLocation(object):
    def __init__(self, postcode, location):
        self.postcode = postcode
        self.location = location

    def __unicode__(self):
        return self.postcode

    def __repr__(self):
        return '<PostcodeLocation: %s - %s>' % (self.postcode, self.location)


class GreendalePostcodeField(GBPostcodeField):
    partial_regex = re.compile(r'^(%s)$' % (GBPostcodeField.outcode_pattern,))

    def clean(self, value):
        full_value = None
        partial_value = None

        # Ensure it's in valid postcode format
        try:
            full_value = super(GreendalePostcodeField, self).clean(value)
        except ValidationError:
            # Try a partial postcode
            postcode = value.upper().strip()

            if not self.partial_regex.search(postcode):
                raise ValidationError(self.error_messages['invalid'])

            partial_value = postcode

        if full_value:
            location = get_postcode_location(value)
            value = PostcodeLocation(value, location)
        elif partial_value:
            location = get_partial_postcode_location(value)
            value = PostcodeLocation(value, location)

        return value
