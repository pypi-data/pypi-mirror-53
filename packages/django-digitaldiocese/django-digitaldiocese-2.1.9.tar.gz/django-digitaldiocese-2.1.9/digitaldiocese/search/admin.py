# from django.contrib import admin
from glitter import block_admin

from . import models
from .forms import SearchBlockAdminForm

block_admin.site.register(models.SearchBlock, form=SearchBlockAdminForm)
block_admin.site.register_block(models.SearchBlock, 'App Blocks')
