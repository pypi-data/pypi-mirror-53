from django.db import models

from digitaldiocese.acny.models import Church, Parish, Person


class VenueDataLinker(models.Model):
    """
    Provides a convenient way of storing and retrieving IDs for churches as
    they are defined in various APIs.

    This allows data from one API to be easily linked to data from other APIs.
    """

    # Our church_id. Allowed to be nullable as will still be worth keeping any
    # other ID lookups intact, even if we've done away with the church.
    church = models.OneToOneField(Church, on_delete=models.SET_NULL, null=True, unique=True)

    # ACNY venue ID can be found in various ACNY calls, e.g.:
    # http://www.achurchnearyou.com/xml/diocese/20/
    acny_venue_id = models.PositiveIntegerField(null=True, blank=True, db_index=True, unique=True)

    def __str__(self):
        return "({church}, {acny_venue_id})".format(
            church=self.church, acny_venue_id=self.acny_venue_id
        )


class ChurchDataLinker(models.Model):
    """
    One ACNY Church can contain multiple ACNY Venues.

    Some APIs (e.g. MyDiocese) reference the ACNY Church ID, but DD works
    mainly at the ACNY Venue level. This model provides a way to retrieve the
    Venues associated with a single ACNY Church.

    The ACNY data is a bit whacky, so have implemented this as quite a loose,
    non-normalised relationship between VenueDataLinker and ChurchDataLinker.
    This allows it to handle discrepencies in data, at the expense of being a
    bit rubbish.

    As more is understood about the API and we gain more confidence in the
    quality of the data, this could be changed to be a standard 1:M
    relationship.
    """

    venue_data_linker = models.ForeignKey('VenueDataLinker', on_delete=models.CASCADE)

    # ACNY church ID can be discovered with an ACNY venue_id:
    # http://www.achurchnearyou.com/xml/venue/4112/
    # It matches the MyDiocese tblchurch.ccref field.
    acny_church_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    # MyDiocese church ID is the primary key for the tblchurch table.
    myd_church_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return "({acny_church_id}, {myd_church_id})".format(acny_church_id=self.acny_church_id,
                                                            myd_church_id=self.myd_church_id)


class ParishDataLinker(models.Model):
    """
    Provides a convenient way of storing and retrieving IDs for churches as
    they are defined in various APIs.

    This allows data from one API to be easily linked to data from other APIs.
    """

    # Our parish_id. Allowed to be nullable as will still be worth keeping any
    # other ID lookups intact, even if we've done away with the parish.
    parish = models.OneToOneField(Parish, on_delete=models.SET_NULL, null=True, unique=True)

    # ACNY parish ID can be discovered in a few places, such as:
    # http://www.achurchnearyou.com/xml/diocese/20/
    # It matches the MyDiocese tblparish.ccref field.
    acny_parish_id = models.PositiveIntegerField(null=True, blank=True, db_index=True, unique=True)

    # MyDiocese parish ID is the primary key for the tblparish table.
    myd_parish_id = models.PositiveIntegerField(null=True, blank=True, db_index=True, unique=True)


class PersonDataLinker(models.Model):
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True, blank=True)
    myd_person_id = models.PositiveIntegerField(null=True, blank=True, db_index=True, unique=True)
