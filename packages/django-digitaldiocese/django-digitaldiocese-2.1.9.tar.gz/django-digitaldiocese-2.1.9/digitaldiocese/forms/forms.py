from django import forms


class EmailAddressForm(forms.Form):
    email = forms.EmailField()

    error_css_class = 'error'
    required_css_class = 'required'
