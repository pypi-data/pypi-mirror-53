from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from glitter.models import Version

from .models import Church, ChurchService, Deanery, Parish, Person, PersonAddress
from .views import ChurchDetailView, DeaneryView


def helper_create_person(**kwargs):
    p = Person(**kwargs)
    return p


class PersonTestCase(TestCase):

    def setUp(self):
        self.p = helper_create_person()
        self.p.save()

    def test_create(self):
        self.assertTrue(self.p.id > 0)

    def test_get_full_name(self):
        name_elements = {
            'title': 'Mr',
            'initials': 'TU',
            'forenames': 'Forenames',
            'surname': 'Surname',
        }
        p = helper_create_person(**name_elements)
        expected = 'Mr Forenames Surname'
        self.assertEqual(p.get_full_name(), expected)

        name_elements['preferred_name'] = 'Preferred'
        p = helper_create_person(**name_elements)
        expected = 'Mr Preferred Surname'
        self.assertEqual(p.get_full_name(), expected)

        name_elements['mailing_name'] = 'Test Mailing Name'
        expected = 'Test Mailing Name'
        p = helper_create_person(**name_elements)
        self.assertEqual(p.get_full_name(), expected)

    def test_get_address_parts(self):
        parts = {
            "address_1": "Test Address 1",
            "address_2": "Test Address 2",
            "address_3": "Test Address 3",
            "address_4": "Test Address 4",
            "address_5": "Test Address 5",
            "town": "Test Town",
            "postcode": "AA1 1AA",
        }
        expected = [
            parts["address_1"],
            parts["address_2"],
            parts["address_3"],
            parts["address_4"],
            parts["address_5"],
            parts["town"],
            parts["postcode"],
        ]
        a = PersonAddress(**parts)
        self.assertListEqual(a.get_address_parts(), expected)

        # empty values shouldn't be included
        parts = {
            "address_1": "Test Address 1",
            "address_2": "Test Address 2",
            "address_3": "",
            "address_5": " ",
            "town": "Test Town",
            "postcode": "AA1 1AA",
        }
        expected = [
            parts["address_1"],
            parts["address_2"],
            parts["town"],
            parts["postcode"],
        ]
        a = PersonAddress(**parts)
        self.assertListEqual(a.get_address_parts(), expected)


class DeaneryTestCase(TestCase):

    def setUp(self):
        self.d = Deanery.objects.create(name='Test Deanery', )

    def test_creating(self):
        self.assertIsInstance(self.d, Deanery)
        self.d.save()
        self.assertIsNotNone(self.d.id)

    def test_absolute_url(self):
        url = self.d.get_absolute_url()
        self.assertIn(str(self.d.id), url)


class ParishTestCase(TestCase):

    def setUp(self):
        self.p = Parish.objects.create(name='Test Parish')

    def test_creating(self):
        self.assertIsInstance(self.p, Parish)
        self.p.save()
        self.assertIsNotNone(self.p.id)


class ChurchTestCase(TestCase):

    def setUp(self):
        p = Parish.objects.create(name='Test Parish')
        d = Deanery.objects.create(name='Test Deanery')

        self.c = Church.objects.create(
            name='Test Church',
            parish=p,
            deanery=d,
            acny_url="http://example.com",
            website="http://example.com",
            location=GEOSGeometry('POINT(10 10)'),
            road="Some road",
            town="Some town",
            county="Some country",
            postcode="AA1 1AA",
            phone_number="01234567890",
            email="test@example.com",
        )

    def test_creating(self):
        self.assertIsInstance(self.c, Church)
        self.c.save()

    def test_absolute_url(self):
        url = self.c.get_absolute_url()
        self.assertIn(str(self.c.id), url)


class ChurchDetailViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        p = Parish.objects.create(name='Test Parish')
        d = Deanery.objects.create(name='Test Deanery')

        self.c_unpublished = Church.objects.create(
            name='Test Church',
            parish=p,
            deanery=d,
            acny_url="http://example.com",
            website="http://example.com",
            location=GEOSGeometry('POINT(10 10)'),
            road="Some road",
            town="Some town",
            county="Some country",
            postcode="AA1 1AA",
            phone_number="01234567890",
            email="test@example.com",
        )
        self.c_published = Church.objects.create(
            name='Test Church',
            parish=p,
            deanery=d,
            acny_url="http://example.com",
            website="http://example.com",
            location=GEOSGeometry('POINT(10 10)'),
            road="Some road",
            town="Some town",
            county="Some country",
            postcode="AA1 1AA",
            phone_number="01234567890",
            email="test@example.com",
        )
        self.c_published.published = True
        p.save()
        d.save()
        self.c_unpublished.save()
        self.c_published.save()

        version = Version(content_type=ContentType.objects.get_for_model(self.c_published),
                          object_id=self.c_published.id,
                          template_name='glitter/acnychurch.html')
        version.generate_version()
        version.save()

        # Point to the current version
        self.c_published.current_version = version
        self.c_published.save()

    def test_unpublished_error(self):
        request = self.factory.get(
            reverse(
                'digitaldiocese-acny:church-detail', kwargs={'church_id': self.c_unpublished.id}
            )
        )

        from glitter.exceptions import GlitterUnpublishedException
        with self.assertRaises(GlitterUnpublishedException):
            ChurchDetailView.as_view()(
                request=request,
                church_id=self.c_unpublished.id
            )

    def test_valid_church(self):
        request = self.factory.get(
            reverse(
                'digitaldiocese-acny:church-detail', kwargs={'church_id': self.c_published.id}
            ),
        )
        request.user = None

        response = ChurchDetailView.as_view()(request=request, church_id=self.c_published.id)
        self.assertEqual(response.status_code, 200)


class DeaneryDetailViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        d = Deanery.objects.create(name='Test Deanery', )
        d.save()
        self.d = d

    def test_valid_deanery(self):
        request = self.factory.get(
            reverse('digitaldiocese-acny:deanery', kwargs={'deanery_id': self.d.id}),
        )

        response = DeaneryView.as_view()(request=request, deanery_id=self.d.id)
        self.assertEqual(response.status_code, 200)


class ChurchServiceTestCase(TestCase):

    def test_set_days_from_acny_bitmask(self):
        bitmask = 1 + 2 + 4
        cs = ChurchService()
        cs.set_days_from_acny_bitmask(bitmask)
        self.assertTrue(cs.saturday)
        self.assertTrue(cs.friday)
        self.assertTrue(cs.thursday)
        self.assertFalse(cs.wednesday)
        self.assertFalse(cs.tuesday)
        self.assertFalse(cs.monday)
        self.assertFalse(cs.sunday)

    def test_set_recurrence_from_acny_bitmask(self):
        bitmask = 1 + 2 + 4
        cs = ChurchService()
        cs.set_recurrence_from_acny_bitmask(bitmask)
        self.assertTrue(cs.every_5th_occ)
        self.assertTrue(cs.every_4th_occ)
        self.assertTrue(cs.every_3rd_occ)
        self.assertFalse(cs.every_2nd_occ)
        self.assertFalse(cs.every_1st_occ)
        self.assertFalse(cs.every_occ)

        # 0 bitmask seems to indicate every occurence
        bitmask = 0
        cs = ChurchService()
        cs.set_recurrence_from_acny_bitmask(bitmask)
        self.assertFalse(cs.every_5th_occ)
        self.assertFalse(cs.every_4th_occ)
        self.assertFalse(cs.every_3rd_occ)
        self.assertFalse(cs.every_2nd_occ)
        self.assertFalse(cs.every_1st_occ)
        self.assertTrue(cs.every_occ)

        # setting all bitmasks just means every occurence
        bitmask = 31
        cs = ChurchService()
        cs.set_recurrence_from_acny_bitmask(bitmask)
        self.assertFalse(cs.every_5th_occ)
        self.assertFalse(cs.every_4th_occ)
        self.assertFalse(cs.every_3rd_occ)
        self.assertFalse(cs.every_2nd_occ)
        self.assertFalse(cs.every_1st_occ)
        self.assertTrue(cs.every_occ)

        # not seen in data, but possible
        bitmask = 31 + 32
        cs = ChurchService()
        cs.set_recurrence_from_acny_bitmask(bitmask)
        self.assertFalse(cs.every_5th_occ)
        self.assertFalse(cs.every_4th_occ)
        self.assertFalse(cs.every_3rd_occ)
        self.assertFalse(cs.every_2nd_occ)
        self.assertFalse(cs.every_1st_occ)
        self.assertTrue(cs.every_occ)

        # just all occurences should work
        bitmask = 32
        cs = ChurchService()
        cs.set_recurrence_from_acny_bitmask(bitmask)
        self.assertFalse(cs.every_5th_occ)
        self.assertFalse(cs.every_4th_occ)
        self.assertFalse(cs.every_3rd_occ)
        self.assertFalse(cs.every_2nd_occ)
        self.assertFalse(cs.every_1st_occ)
        self.assertTrue(cs.every_occ)
