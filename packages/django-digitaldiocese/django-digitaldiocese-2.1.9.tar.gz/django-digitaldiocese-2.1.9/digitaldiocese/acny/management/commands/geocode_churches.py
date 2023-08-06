from django.core.management.base import BaseCommand
from django.forms import ValidationError

from digitaldiocese.acny.models import Church
from digitaldiocese.acny.utils import get_postcode_location
from tqdm import tqdm


class Command(BaseCommand):

    def handle(self, *args, **options):
        churches = Church.objects.filter(location__isnull=True).exclude(postcode='')
        self.update_churches(churches)

    def update_churches(self, churches):
        for church in tqdm(churches):
            try:
                location = get_postcode_location(church.postcode)
            except ValidationError:
                # No location found for postcode
                continue

            church.location = location
            church.save()
