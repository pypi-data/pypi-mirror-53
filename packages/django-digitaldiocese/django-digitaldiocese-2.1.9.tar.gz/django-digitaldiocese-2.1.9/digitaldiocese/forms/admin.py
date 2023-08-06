# -*- coding: utf-8 -*-

from glitter import block_admin

from .models import EmailAddressFormBlock

block_admin.site.register(EmailAddressFormBlock)
block_admin.site.register_block(EmailAddressFormBlock, 'Forms')
