from django import forms

from .fields import GreendalePostcodeField


class PostcodeForm(forms.Form):
    q = GreendalePostcodeField(label='Postcode')
