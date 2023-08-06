from django.test import TestCase

from digitaldiocese.acny.models import Church, Deanery, Parish


def helper_create_church():
    d = Deanery(name="Test Deanery")
    d.save()
    p = Parish(name="Test Parish")
    p.save()
    c = Church(name="Test Church", parish=p, deanery=d, acny_url="http://example.com",
               road="", town="", county="", postcode="", phone_number="", email="")
    c.save()
    return c


def helper_create_parish():
    p = Parish(name="Test Parish")
    p.save()
    return p


class ChurchDataLinkerTestCase(TestCase):
    pass


class ParishDataLinkerTestCase(TestCase):
    pass
