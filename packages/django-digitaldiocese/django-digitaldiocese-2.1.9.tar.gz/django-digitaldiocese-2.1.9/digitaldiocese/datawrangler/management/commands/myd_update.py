from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('myd_update_people', *args, **options)
        call_command('myd_update_roles', *args, **options)
        call_command('myd_update_parish_geo', *args, **options)
