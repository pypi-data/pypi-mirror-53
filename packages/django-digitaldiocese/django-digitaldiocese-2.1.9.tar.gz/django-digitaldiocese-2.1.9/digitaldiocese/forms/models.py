# -*- coding: utf-8 -*-

from glitter.blocks.form.models import BaseFormBlock


class EmailAddressFormBlock(BaseFormBlock):
    form_class = 'digitaldiocese.forms.forms.EmailAddressForm'

    class Meta:
        verbose_name = 'email address submission'
