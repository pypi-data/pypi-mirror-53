from django.forms.widgets import Select

from glitter import block_admin
from glitter.widgets import CustomRelatedFieldWidgetWrapper

from .models import DioceseCarouselBlock


class DioceseCarouselBlockAdmin(block_admin.BlockModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'carousel':
            formfield.widget = CustomRelatedFieldWidgetWrapper(
                widget=Select(),
                rel=db_field.rel,
                admin_site=self.admin_site,
                can_add_related=True,
                can_change_related=True,
            )
        return formfield


block_admin.site.register(DioceseCarouselBlock, DioceseCarouselBlockAdmin)
block_admin.site.register_block(DioceseCarouselBlock, 'Media')
