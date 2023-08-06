# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from glitter.assets.fields import AssetForeignKey
from glitter.mixins import GlitterMixin
from glitter.models import BaseBlock
from simplejson import JSONEncoderForHTML

from . import choices
from .utils import place_geojson


class Archdeaconry(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    published = models.BooleanField(default=True, db_index=True)
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    worthers_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'archdeaconries'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('digitaldiocese-acny:archdeaconry', kwargs={'archdeaconry_id': self.id, })


@python_2_unicode_compatible
class Deanery(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    legacy_acny_id = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    published = models.BooleanField(default=True, db_index=True)
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    worthers_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'deaneries'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('digitaldiocese-acny:deanery', kwargs={'deanery_id': self.id, })


class Benefice(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    published = models.BooleanField(default=True, db_index=True)
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    worthers_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'benefices'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('digitaldiocese-acny:benefice', kwargs={'benefice_id': self.id, })


@python_2_unicode_compatible
class Parish(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    legacy_acny_id = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    boundary_data = models.TextField(blank=True, default="")
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    worthers_updated = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('digitaldiocese-acny:parish', kwargs={'parish_id': self.id, })

    class Meta:
        verbose_name_plural = 'parishes'
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Church(GlitterMixin, models.Model):
    name = models.CharField(max_length=200, db_index=True)
    legacy_acny_id = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    worthers_updated = models.DateTimeField(null=True, blank=True)

    place_type = models.PositiveSmallIntegerField(
        choices=choices.PLACE_TYPE_CHOICES, default=choices.PLACE_TYPE_CHURCH
    )

    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.SET_NULL)
    deanery = models.ForeignKey(Deanery, null=True, blank=True, on_delete=models.SET_NULL)
    archdeaconry = models.ForeignKey(
        Archdeaconry, null=True, blank=True, on_delete=models.SET_NULL
    )
    benefice = models.ForeignKey(
        Benefice, null=True, blank=True, on_delete=models.SET_NULL
    )
    acny_url = models.URLField('ACNY URL')
    website = models.URLField(blank=True)
    location = models.PointField(null=True, blank=True, srid=4326)
    road = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    postcode = models.CharField(max_length=50)
    image = AssetForeignKey('glitter_assets.Image', blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    description = models.TextField(blank=True, default="")
    patron = models.CharField(max_length=255, blank=True, default="")
    charity_number = models.CharField(max_length=20, blank=True, default="")
    built = models.CharField(max_length=200, blank=True, default="")
    architect = models.CharField(max_length=200, blank=True, default="")

    objects = models.GeoManager()

    class Meta(GlitterMixin.Meta):
        verbose_name_plural = 'churches'
        ordering = ('name',)

    def __str__(self):
        name = self.name.title()
        if self.postcode:
            name += ', {postcode}'.format(postcode=self.postcode.upper())
        return name

    def get_absolute_url(self):
        return reverse('digitaldiocese-acny:church-detail', kwargs={'church_id': self.id, })

    def address_list(self):
        address_list = []

        for i in (self.road, self.town, self.postcode):
            if i:
                address_list.append(i)

        return address_list

    def address(self):
        return ', '.join(self.address_list())

    def get_relevant_people(self):
        """
        Get a list of all people relevant to this Church.

        A person is relevant if they have a role directly with the Church, or have an overseeing
        role further up the hierarchy.
        """
        direct_people = self.people.all()

        relevant_benefice_people = []
        if self.benefice:
            chuch_relevant_benefice_roles = getattr(
                settings, 'CHURCH_RELEVANT_BENEFICE_ROLES', []
            )
            if len(chuch_relevant_benefice_roles) > 0:
                relevant_benefice_people = self.benefice.benefice_people.filter(
                    role_name__in=chuch_relevant_benefice_roles
                )

        return list(relevant_benefice_people) + list(direct_people)


class ChurchRole(models.Model):
    """
    Join table between Person and Church.

    Used to define the role of the person within a Church.
    """
    church = models.ForeignKey('Church', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='people')
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='roles')
    role_name = models.CharField(max_length=255, blank=True, default="")
    role_description = models.TextField(blank=True)
    myd_tjppid = models.PositiveIntegerField(db_index=True, null=True, blank=True, unique=False)
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=False)
    worthers_updated = models.DateTimeField(null=True, blank=True)


class BeneficeRole(models.Model):
    """
    Join table between Person and Benefice.

    Used to define the role of the person within a Benefice.
    """
    benefice = models.ForeignKey(
        'Benefice', null=True, blank=True, on_delete=models.CASCADE, related_name='benefice_people'
    )
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='benefice_roles')
    role_name = models.CharField(max_length=255, blank=True, default='')
    role_description = models.TextField(blank=True)
    worthers_id = models.PositiveIntegerField(null=True, blank=True, unique=False)
    worthers_updated = models.DateTimeField(null=True, blank=True)


class Person(models.Model):
    """
    A single person.

    Fields influenced by the MyDiocese database structure, hence some of the
    crazy max_lengths on CharFields.
    """

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_MALE, 'male'),
        (GENDER_FEMALE, 'female'),
    )

    title = models.CharField(max_length=100, blank=True, default="")
    initials = models.CharField(max_length=50, blank=True, default="")
    forenames = models.CharField(max_length=200, blank=True, default="")
    surname = models.CharField(max_length=200, blank=True, default="")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    preferred_name = models.CharField(max_length=200, blank=True, default="")

    image = AssetForeignKey('glitter_assets.Image', null=True, on_delete=models.PROTECT)

    # Mailing name is the full name, inlcuding title, preferred_name, surname,
    # etc. Sometimes NULL in the MyD database, and sometimes contains manually
    # entered elements (i.e. can't rely on just concatenating other fields to
    # create the mailing name).
    mailing_name = models.CharField(max_length=255, blank=True, default="")

    church = models.ManyToManyField(
        'Church', through='ChurchRole', through_fields=('person', 'church')
    )

    myd_person_id = models.PositiveIntegerField(unique=True, null=True, blank=True, db_index=True)
    worthers_id = models.PositiveIntegerField(
        unique=True, null=True, blank=True, db_index=True
    )
    worthers_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'people'
        ordering = ('surname', 'forenames')

    def __str__(self):
        out = '{surname}, {forenames} - {full_name}'.format(
            surname=self.surname, forenames=self.forenames, full_name=self.get_full_name(),
        )
        return out

    def get_full_name(self):
        """
        Retrieve a name for this person which can be used throughout the site.
        """
        if self.mailing_name != "":
            return self.mailing_name

        forename = self.forenames
        if self.preferred_name != "":
            forename = self.preferred_name

        full_name = "{title} {forename} {surname}".format(title=self.title,
                                                          forename=forename,
                                                          surname=self.surname)
        return full_name.strip()

    def get_absolute_url(self):
        return reverse('digitaldiocese-acny:person-detail', kwargs={'person_id': self.id, })


class PersonEmail(models.Model):

    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='emails')

    # friendly name for email, e.g. Work, Office, etc.
    label = models.CharField(max_length=50, blank=True)
    address = models.EmailField(max_length=150)

    # Can't be unique as 1 MyD addressbook entry has 2 emails :(
    myd_address_id = models.PositiveIntegerField(
        unique=False, null=True, blank=True, db_index=True
    )

    def __str__(self):
        return "{label}: {email}".format(email=self.address, label=self.label)


class PersonAddress(models.Model):

    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='addresses')

    # friendly name for the address. e.g. Work, Office, etc.
    label = models.CharField(max_length=100, blank=True, default="")
    is_primary = models.BooleanField(default=False)
    address_1 = models.CharField(max_length=200, blank=True, default="")
    address_2 = models.CharField(max_length=200, blank=True, default="")
    address_3 = models.CharField(max_length=200, blank=True, default="")
    address_4 = models.CharField(max_length=200, blank=True, default="")
    address_5 = models.CharField(max_length=200, blank=True, default="")
    town = models.CharField(max_length=200, blank=True, default="")
    postcode = models.CharField(max_length=50, blank=True, default="")

    myd_address_id = models.PositiveIntegerField(unique=True, null=True, blank=True, db_index=True)

    def __str__(self):
        return "{label}: {address}".format(label=self.label, address=self.address_1)

    def get_address_parts(self):
        part_fields = [
            "address_1",
            "address_2",
            "address_3",
            "address_4",
            "address_5",
            "town",
            "postcode",
        ]
        out = []
        for field_name in part_fields:
            value = getattr(self, field_name)
            if value.strip() != "":
                out.append(value.strip())
        return out


class PersonPhone(models.Model):
    TYPE_UNKNOWN = 'unknown'
    TYPE_HOME = 'home'
    TYPE_OFFICE = 'office'
    TYPE_MOBILE = 'mobile'
    TYPE_FAX = 'fax'
    TYPE_CHOICES = (
        (TYPE_UNKNOWN, ''),
        (TYPE_HOME, 'home'),
        (TYPE_OFFICE, 'office'),
        (TYPE_MOBILE, 'mobile'),
        (TYPE_FAX, 'fax'),
    )

    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='phone_numbers')

    phone_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    number = models.CharField(max_length=50)

    # Can't be unique 1 MyD addressbook entry has mutliple phone numbers :(
    myd_address_id = models.PositiveIntegerField(
        unique=False, null=True, blank=True, db_index=True
    )

    def __str__(self):
        return "{type}: {number}".format(type=self.phone_type, number=self.number)


class ChurchService(models.Model):
    """
    A single, recurring service for a church.
    """
    church = models.ForeignKey('Church', on_delete=models.CASCADE, related_name='services')

    name = models.CharField(max_length=255)
    notes = models.TextField('event notes', default="", blank=True)

    # Data contained in ACNY which relates purely to scheduling notes.
    # E.g. "not on the first Thursday in Lent - this service is transferred to
    # Ash Wednesday"
    r_notes = models.TextField('scheduling notes', max_length=255, blank=True, default="")

    labels = models.ManyToManyField("ChurchServiceLabel")

    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    duration = models.PositiveIntegerField(help_text='minutes', null=True, blank=True)

    recurring = models.BooleanField(default=False)

    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)

    # Using ACNY's convention for specifying the recurrence of an event...
    # which might need to expanded/changed for other recurrence mechanisms
    # in the future. However this setup at least allows the recurrence to be
    # specified like:
    # "1st and 3rd Sunday of each month", "Every Tuesday" etc.
    every_1st_occ = models.BooleanField('every 1st occurence in a month', default=False)
    every_2nd_occ = models.BooleanField('every 2nd occurence in a month', default=False)
    every_3rd_occ = models.BooleanField('every 3rd occurence in a month', default=False)
    every_4th_occ = models.BooleanField('every 4th occurence in a month', default=False)
    every_5th_occ = models.BooleanField('every 5th occurence in a month', default=False)
    every_occ = models.BooleanField('every occurence', default=False)

    def __str__(self):
        return self.name

    def has_days_set(self):
        return len(self.get_set_days()) > 0

    def set_days_from_acny_bitmask(self, bitmask):
        """
        Sets the approriate days based upon an ACNY weekdays bitmask.
        """
        self.saturday = bitmask & 1
        self.friday = bitmask & 2
        self.thursday = bitmask & 4
        self.wednesday = bitmask & 8
        self.tuesday = bitmask & 16
        self.monday = bitmask & 32
        self.sunday = bitmask & 64

    def set_recurrence_from_acny_bitmask(self, bitmask):
        """
        Sets the approriate recurrence based upon an ACNY weeks bitmask.
        """
        # Data shows special cases to set every occurence. Users selecting all
        # days or not setting any also indicates every day.
        if bitmask == 0 or bitmask >= 31:
            bitmask = 32
        self.every_5th_occ = bitmask & 1
        self.every_4th_occ = bitmask & 2
        self.every_3rd_occ = bitmask & 4
        self.every_2nd_occ = bitmask & 8
        self.every_1st_occ = bitmask & 16
        self.every_occ = bitmask & 32

    def get_days(self):
        days = ["sunday",
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                ]
        set_days = []
        for day in days:
            if getattr(self, day) is True:
                set_days.append(day)
        return set_days

    def get_friendly_recurrences(self):
        mapping = {
            "every_1st_occ": "1st",
            "every_2nd_occ": "2nd",
            "every_3rd_occ": "3rd",
            "every_4th_occ": "4th",
            "every_5th_occ": "5th",
        }
        recurrence = []

        for field, text in mapping.items():
            if getattr(self, field) is True:
                recurrence.append(text)
        if len(recurrence) == 5:
            recurrence = []
        recurrence.sort()
        return recurrence


class ChurchServiceLabel(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class PostcodeSearchBlock(BaseBlock):

    class Meta:
        verbose_name = 'postcode search'


class PersonBlock(BaseBlock):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True)

    class Meta:
        verbose_name = 'person summary'

    def __str__(self):
        return str(self.person)


class ChurchBlock(BaseBlock):
    church = models.ForeignKey('Church', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Church/School summary'

    def __str__(self):
        return str(self.church)

    def get_map_json(self):
        church_qs = Church.objects.filter(id=self.church.id)
        map_json = JSONEncoderForHTML().encode(place_geojson(church_qs))
        return map_json


class RoleBlock(BaseBlock):
    benefice = models.ForeignKey('Benefice', on_delete=models.SET_NULL, null=True, blank=True)
    church = models.ForeignKey('Church', on_delete=models.SET_NULL, null=True, blank=True)
    role_name = models.CharField(max_length=255, blank=True)

    content = models.TextField(blank=True)

    def get_roles(self):
        roles = []
        benefice_roles = []
        church_roles = []

        if self.benefice or self.church:
            if self.benefice:
                benefice_roles = self.benefice.benefice_people.filter(role_name=self.role_name)

            if self.church:
                church_roles = self.church.people.filter(role_name=self.role_name)

        else:
            benefice_roles = BeneficeRole.objects.filter(role_name=self.role_name)
            church_roles = ChurchRole.objects.filter(role_name=self.role_name)

        roles = list(benefice_roles) + list(church_roles)
        return roles
