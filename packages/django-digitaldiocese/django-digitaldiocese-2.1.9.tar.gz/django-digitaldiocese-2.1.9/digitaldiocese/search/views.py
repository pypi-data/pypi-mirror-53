# -*- coding: utf-8 -*-

import re

from haystack.views import SearchView as HaystackSearchView

from digitaldiocese.acny.views import PostcodeSearchView

from .forms import SearchForm


class SearchView(HaystackSearchView):
    results_per_page = 10

    def extra_context(self):
        extra = super(SearchView, self).extra_context()

        # Filtering help
        extra.update({
            'content_type_list': SearchForm.MODEL_CHOICES,
            'total_found': self.results.count(),
        })

        # Show form choices
        if self.form.is_valid():
            extra.update(self.form.cleaned_data)

        return extra

    def create_response(self):
        # If it looks like the user is searching for a postcode, then presume the user is
        # searching by location and have the PostcodeSearchView render the view.
        #
        # Postcode checking logic adapted from:
        # https://github.com/django/django-localflavor/blob/master/localflavor/gb/forms.py
        #
        # See here for a good brief description of postcode structure:
        # http://www.bph-postcodes.co.uk/guidetopc.cgi

        # Postcodes are made up of "outcode" (e.g. "B90"), and the "incode" (e.g. "8AJ")
        outcode_pattern = (
            '[A-PR-UWYZ]([0-9]{1,2}|([A-HIK-Y][0-9](|[0-9]|[ABEHMNPRVWXY]))|[0-9][A-HJKSTUW])'
        )
        incode_pattern = '[0-9][ABD-HJLNP-UW-Z]{2}'

        # Regex to check for a complete postcode
        postcode_regex = re.compile(r'^(GIR 0AA|{outcode_pattern} {incode_pattern})$'.format(
            outcode_pattern=outcode_pattern, incode_pattern=incode_pattern,
        ))

        # Regex to check for just the outcode
        outcode_regex = re.compile(r'^{outcode_pattern}'.format(outcode_pattern=outcode_pattern))

        # A regex which can be used to insert a space into the postcode in case user has entered
        # postcode without a space, e.g. "B908AJ".
        space_regex = re.compile(r' *({incode_pattern})$'.format(incode_pattern=incode_pattern))

        if self.query:
            postcode = self.query.upper().strip()

            # Add a space as necessary before checking
            postcode = space_regex.sub(r' \1', postcode)

            if postcode_regex.search(postcode) or outcode_regex.search(postcode):
                return PostcodeSearchView.as_view()(self.request)

        return super(SearchView, self).create_response()
