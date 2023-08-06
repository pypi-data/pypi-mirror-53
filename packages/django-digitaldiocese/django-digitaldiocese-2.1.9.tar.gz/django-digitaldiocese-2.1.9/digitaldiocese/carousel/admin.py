from django.contrib import admin

from .models import DioceseCarousel, DioceseCarouselSlide


class DioceseCarouselImageInline(admin.StackedInline):
    model = DioceseCarouselSlide
    extra = 1


@admin.register(DioceseCarousel)
class DioceseCarouselAdmin(admin.ModelAdmin):
    inlines = [DioceseCarouselImageInline]
