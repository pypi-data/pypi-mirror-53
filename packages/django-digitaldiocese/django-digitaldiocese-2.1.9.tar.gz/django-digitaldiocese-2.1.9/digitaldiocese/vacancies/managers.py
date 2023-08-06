from django.db import models
from django.db.models import Q
from django.utils import timezone


class VacancyManager(models.Manager):
    def active(self):
        return self.model.objects.published().exclude(
            display_until__lte=timezone.now()
        ).filter(
            Q(display_from__isnull=True) | Q(display_from__lte=timezone.now())
        )
