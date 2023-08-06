from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from digitaldiocese.acny.models import Person, PersonAddress, PersonEmail, PersonPhone
from digitaldiocese.datawrangler.models import ChurchDataLinker
from MySQLdb import connect
from MySQLdb.cursors import DictCursor


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_myd_people()


def update_myd_people():
    if settings.MYD_DB_HOST is None:
        raise CommandError("MyDiocese DB settings not configured.")
    db = connect(host=settings.MYD_DB_HOST,
                 port=int(settings.MYD_DB_PORT),
                 user=settings.MYD_DB_USERNAME,
                 passwd=settings.MYD_DB_PASSWORD,
                 db=settings.MYD_DB_DATABASE)

    # get all church ids
    acny_church_ids = get_acny_church_ids()
    print("Will process people for {church_count} churches".format(
        church_count=len(acny_church_ids)
    ))

    # get all myd people for those church ids
    all_people_data = get_myd_people_data(acny_church_ids, db)
    print("There's data on {people_count} people...".format(people_count=len(all_people_data)))

    # get already added people
    existing_people = get_existing_people_by_myd_person_id()
    print("There's currently {existing_count} people in the system...".format(
        existing_count=len(existing_people)))

    add_new_people(all_people_data, existing_people)
    update_existing_people(all_people_data, existing_people)
    remove_old_people(all_people_data, existing_people)

    # contact details

    # ensure known people are up to date
    existing_people = get_existing_people_by_myd_person_id()
    current_person_ids = all_people_data.keys()

    cd_by_addressid, addressid_by_person_id = get_myd_contact_data(current_person_ids, db)
    print("There's {ab_count} addressbook entries to process...".format(
        ab_count=len(cd_by_addressid)
    ))

    process_addresses(cd_by_addressid, addressid_by_person_id, existing_people)

    process_phone_numbers(cd_by_addressid, addressid_by_person_id, existing_people)

    process_emails(cd_by_addressid, addressid_by_person_id, existing_people)


def process_emails(cd_by_addressid, addressid_by_person_id, existing_people):
    existing_emails = PersonEmail.objects.filter(
        myd_address_id__isnull=False
    )
    existing_emails_by_person_id = {}
    existing_emails_by_address_id = {}
    for ee in existing_emails:
        if ee.person.myd_person_id not in existing_emails_by_person_id:
            existing_emails_by_person_id[ee.person.myd_person_id] = []
        existing_emails_by_person_id[ee.person.myd_person_id].append(ee)

        if ee.myd_address_id not in existing_emails_by_address_id:
            existing_emails_by_address_id[ee.myd_address_id] = []
        existing_emails_by_address_id[ee.myd_address_id].append(ee)

    print("There's currently {email_count} MyD emails in the system...".format(
        email_count=len(existing_emails_by_address_id)))

    add_emails(cd_by_addressid, existing_emails_by_address_id, existing_people)
    update_emails(cd_by_addressid, existing_emails_by_address_id, existing_people)
    delete_emails(cd_by_addressid, existing_emails_by_address_id, existing_people)


@transaction.atomic
def add_emails(cd_by_addressid, existing_emails_by_address_id, existing_people):
    missing_emails = list(set(cd_by_addressid.keys()) - set(existing_emails_by_address_id.keys()))
    print("There's potentially {missing_count} emails to add...".format(
        missing_count=len(missing_emails)
    ))

    added_emails = 0
    for missing_address_id in missing_emails:
        address_data = cd_by_addressid[missing_address_id]
        person = existing_people[address_data['personid']]
        emails = populate_emails(email1=PersonEmail(), email2=PersonEmail(),
                                 address_data=address_data, person=person)

        for email in emails:
            if email is not False:
                email.save()
                added_emails += 1
    print(("Added {added_emails} emails (and skipped the others)!").format(
        added_emails=added_emails,
    ))


@transaction.atomic
def update_emails(cd_by_addressid, existing_emails_by_address_id, existing_people):
    updated_count = 0
    for addressid, cd in cd_by_addressid.items():
        try:
            emails = existing_emails_by_address_id[addressid]
        except KeyError:
            # an address which has only just been added
            continue
        person = existing_people[cd['personid']]

        # HACK: just presuming the person only has 2 emails. If emails are
        # added via other methods, then they could get lost here.
        try:
            email1 = emails[0]
        except IndexError:
            email1 = None

        try:
            email2 = emails[1]
        except IndexError:
            email2 = None

        updated_emails = populate_emails(
            email1=email1, email2=email2, address_data=cd, person=person
        )

        for up in updated_emails:
            if up is not False:
                up.save()
                updated_count += 1

    print("Updated {updated_count} emails!".format(updated_count=updated_count))


def delete_emails(cd_by_addressid, existing_emails_by_address_id, existing_people):
    to_remove = list(set(existing_emails_by_address_id.keys()) - set(cd_by_addressid.keys()))
    PersonEmail.objects.filter(myd_address_id__in=to_remove).delete()
    print("Removed {removed_count} old emails!".format(removed_count=len(to_remove)))


def populate_emails(email1, email2, address_data, person):
    if (email1 is None or address_data['email'] is None or address_data['emailhide'] == 1):
        email1 = False
    else:
        email1.person = person
        email1.myd_address_id = address_data['addressid']
        email1.label = address_data['emaildescr'] or ""
        email1.address = address_data['email']

    if (email2 is None or address_data['email2'] is None or address_data['email2hide'] == 1):
        email2 = False
    else:
        email2.person = person
        email2.myd_address_id = address_data['addressid']
        email2.label = address_data['emaildescr'] or ""
        email2.address = address_data['email2']

    return (email1, email2)


def process_phone_numbers(cd_by_addressid, addressid_by_person_id, existing_people):
    existing_phones = PersonPhone.objects.filter(myd_address_id__isnull=False)
    existing_phones_by_person_id = {}
    existing_phones_by_address_id = {}
    for ep in existing_phones:
        if ep.person.myd_person_id not in existing_phones_by_person_id:
            existing_phones_by_person_id[ep.person.myd_person_id] = []
        existing_phones_by_person_id[ep.person.myd_person_id].append(ep)

        if ep.myd_address_id not in existing_phones_by_address_id:
            existing_phones_by_address_id[ep.myd_address_id] = []
        existing_phones_by_address_id[ep.myd_address_id].append(ep)

    print(("There's currently {phone_count} MyD phones in the system...").format(
        phone_count=len(existing_phones_by_address_id)))

    add_phones(cd_by_addressid, existing_phones_by_address_id, existing_people)
    update_phones(cd_by_addressid, existing_phones_by_address_id, existing_people)
    delete_phones(cd_by_addressid, existing_phones_by_address_id, existing_people)


@transaction.atomic
def add_phones(cd_by_addressid, existing_phones_by_address_id, existing_people):
    missing_phones = list(set(cd_by_addressid.keys()) - set(existing_phones_by_address_id.keys()))
    print("There's potentially {missing_count} phones to add...".format(
        missing_count=len(missing_phones)
    ))

    added_phones = 0
    for missing_address_id in missing_phones:
        address_data = cd_by_addressid[missing_address_id]
        person = existing_people[address_data['personid']]
        phones = populate_phone(phonehome=PersonPhone(),
                                phoneoffice=PersonPhone(),
                                phonemobile=PersonPhone(),
                                phonefax=PersonPhone(),
                                address_data=address_data,
                                person=person)

        for phone in phones:
            if phone is not False:
                phone.save()
                added_phones += 1
    print(("Added {added_phones} phones (and skipped the others)!").format(
        added_phones=added_phones,
    ))


@transaction.atomic
def update_phones(cd_by_addressid, existing_phones_by_address_id, existing_people):
    updated_count = 0
    for addressid, cd in cd_by_addressid.items():
        try:
            phones = existing_phones_by_address_id[addressid]
        except KeyError:
            # an address which has only just been added
            continue
        person = existing_people[cd['personid']]

        phonehome = None
        phoneoffice = None
        phonemobile = None
        phonefax = None
        for p in phones:
            if p.phone_type == PersonPhone.TYPE_HOME:
                phonehome = p
            if p.phone_type == PersonPhone.TYPE_OFFICE:
                phoneoffice = p
            if p.phone_type == PersonPhone.TYPE_MOBILE:
                phonemobile = p
            if p.phone_type == PersonPhone.TYPE_FAX:
                phonefax = p

        updated_phones = populate_phone(
            phonehome=phonehome, phoneoffice=phoneoffice, phonemobile=phonemobile,
            phonefax=phonefax, address_data=cd, person=person
        )

        for up in updated_phones:
            if up is not False:
                up.save()
                updated_count += 1

    print("Updated {updated_count} phones!".format(updated_count=updated_count))


def delete_phones(cd_by_addressid, existing_phones_by_address_id, existing_people):
    to_remove = list(
        set(existing_phones_by_address_id.keys()) -
        set(cd_by_addressid.keys())
    )
    PersonPhone.objects.filter(myd_address_id__in=to_remove).delete()
    print("Removed {removed_count} old phone numbers!".format(removed_count=len(to_remove)))


def populate_phone(phonehome, phoneoffice, phonemobile, phonefax, address_data, person):
    if (
        phonehome is None or address_data['phonehome'] is None or
        address_data['phonehomehide'] == 1
    ):
        phonehome = False
    else:
        phonehome.myd_address_id = address_data['addressid']
        phonehome.person = person
        phonehome.phone_type = PersonPhone.TYPE_HOME
        phonehome.number = address_data['phonehome'].strip()

    if (
        phoneoffice is None or address_data['phoneoffice'] is None or
        address_data['phoneofficehide'] == 1
    ):
        phoneoffice = False
    else:
        phoneoffice.myd_address_id = address_data['addressid']
        phoneoffice.person = person
        phoneoffice.phone_type = PersonPhone.TYPE_HOME
        phoneoffice.number = address_data['phoneoffice'].strip()

    if (
        phonemobile is None or address_data['phonemobile'] is None or
        address_data['phonemobilehide'] == 1
    ):
        phonemobile = False
    else:
        phonemobile.myd_address_id = address_data['addressid']
        phonemobile.person = person
        phonemobile.phone_type = PersonPhone.TYPE_HOME
        phonemobile.number = address_data['phonemobile'].strip()

    if (phonefax is None or address_data['fax'] is None or address_data['faxhide'] == 1):
        phonefax = False
    else:
        phonefax.myd_address_id = address_data['addressid']
        phonefax.person = person
        phonefax.phone_type = PersonPhone.TYPE_HOME
        phonefax.number = address_data['fax'].strip()

    return(phonehome, phoneoffice, phonemobile, phonefax)


def process_addresses(cd_by_addressid, addressid_by_person_id, existing_people):
    existing_addresses = PersonAddress.objects.filter(myd_address_id__isnull=False)
    existing_addresses_by_person_id = {}
    existing_addresses_by_address_id = {}
    for ea in existing_addresses:
        existing_addresses_by_person_id[ea.person.myd_person_id] = ea
        existing_addresses_by_address_id[ea.myd_address_id] = ea
    print("There's currently {address_count} MyD addresses in the system...".format(
        address_count=len(existing_addresses_by_address_id)))

    add_addresses(cd_by_addressid, existing_addresses_by_address_id, existing_people)
    update_addresses(cd_by_addressid, existing_addresses_by_address_id, existing_people)
    delete_addresses(cd_by_addressid, existing_addresses_by_address_id, existing_people)


def delete_addresses(cd_by_addressid, existing_addresses_by_address_id, existing_people):
    to_remove = list(set(existing_addresses_by_address_id.keys()) - set(cd_by_addressid.keys()))
    PersonAddress.objects.filter(myd_address_id__in=to_remove).delete()
    print("Removed {removed_count} old addresses!".format(removed_count=len(to_remove)))


@transaction.atomic
def update_addresses(cd_by_addressid, existing_addresses_by_address_id, existing_people):
    updated_count = 0
    for addressid, cd in cd_by_addressid.items():
        try:
            address = existing_addresses_by_address_id[addressid]
        except KeyError:
            # an address which has only just been added
            continue
        person = existing_people[cd['personid']]
        address = populate_address(address, cd, person)
        address.save()
        updated_count += 1
    print("Updated {updated_count} addresses!".format(updated_count=updated_count))


@transaction.atomic
def add_addresses(cd_by_addressid, existing_addresses_by_address_id, existing_people):
    missing_addresses = list(
        set(cd_by_addressid.keys()) - set(existing_addresses_by_address_id.keys())
    )
    print("There's {missing_count} addresses to add...".format(
        missing_count=len(missing_addresses)
    ))

    added_addresses = 0
    skipped_addresses = 0
    for missing_address_id in missing_addresses:
        address_data = cd_by_addressid[missing_address_id]
        person = existing_people[address_data['personid']]
        address = populate_address(PersonAddress(), address_data, person)
        if address is False:
            skipped_addresses += 1
        else:
            address.save()
            added_addresses += 1
    print("Added {added_addresses} and skipped {skipped_addresses} addresses!".format(
        added_addresses=added_addresses, skipped_addresses=skipped_addresses, ))


def populate_address(address, address_data, person):
    if (address_data['address1'] is None or address_data['addresshide'] == 1):
        return False

    address.person = person
    address.myd_address_id = address_data['addressid']
    address.is_primary = bool(address_data['isprimary'])
    address.label = address_data['addressname'] or ""
    address.address_1 = address_data['address1'] or ""
    address.address_2 = address_data['address2'] or ""
    address.address_3 = address_data['address3'] or ""
    address.address_4 = address_data['address4'] or ""
    address.address_5 = address_data['address5'] or ""
    address.town = address_data['town'] or ""
    address.postcode = address_data['postcode'] or ""
    return address


def get_myd_contact_data(person_ids, db):
    if len(person_ids) == 0:
        return {}, {}

    c = db.cursor(cursorclass=DictCursor)

    # MySQLdb is whacky when using a list of things for "WHERE x IN (x, y, z)"
    # type queries. See here for more information:
    # http://stackoverflow.com/questions/589284/imploding-a-list-for-use-in-a-python-mysqldb-in-clause
    placeholders = ', '.join(['%s'] * len(person_ids))
    sql = """
SELECT *
FROM tbladdressbook AS ab
WHERE ab.personid in ({placeholders})
GROUP BY ab.personid;""".format(placeholders=placeholders)

    # Make sure you're on Python 3.5 or above if you're getting the following
    # error:
    #     SyntaxError: can use starred expression only as assignment target
    c.execute(sql, (*person_ids, ))
    result_dict = c.fetchallDict()

    # each person can have multiple addresses, so structure our data to make
    # processing that easier
    all_contact_data_by_address_id = {}
    all_addressid_by_person_id = {}

    for cd in result_dict:
        myd_person_id = cd['personid']
        address_id = cd['addressid']
        all_contact_data_by_address_id[address_id] = cd

        if myd_person_id not in all_addressid_by_person_id:
            all_addressid_by_person_id[myd_person_id] = []
        all_addressid_by_person_id[myd_person_id].append(address_id)

    return all_contact_data_by_address_id, all_addressid_by_person_id


def remove_old_people(all_people_data, existing_people):
    old_person_ids = list(set(existing_people.keys()) - set(all_people_data.keys()))
    Person.objects.filter(myd_person_id__in=old_person_ids).delete()
    print("Removed {deleted_count} old users!".format(deleted_count=len(old_person_ids)))


@transaction.atomic
def update_existing_people(all_people_data, existing_people):
    updated_count = 0
    for myd_person_id, person_data in all_people_data.items():
        try:
            person = existing_people[myd_person_id]
        except KeyError:
            continue
        person = populate_person(person, all_people_data[myd_person_id])
        person.save()
        updated_count += 1
    print("Updated {updated_count} users!".format(updated_count=updated_count))


def add_new_people(all_people_data, existing_people):
    new_person_ids = list(set(all_people_data.keys()) - set(existing_people.keys()))
    new_person_data = []
    for new_pid in new_person_ids:
        new_person_data.append(all_people_data[new_pid])
    print("There's {new_count} new people to add...".format(new_count=len(new_person_data)))
    create_people_from_data(new_person_data)


def populate_person(person, person_data):
    person.myd_person_id = person_data['PersonID']
    person.title = person_data['Title'] or ""
    person.initials = person_data['Initials'] or ""
    person.forenames = person_data['Forenames'] or ""
    person.surname = person_data['Surname'] or ""
    try:
        person.gender = person_data['Gender'].lower()
    except AttributeError:
        pass
    person.preferred_name = person_data['PreferredName'] or ""
    person.mailing_name = person_data['MailingTitle'] or ""

    return person


@transaction.atomic
def create_people_from_data(people_data):
    created_count = 0
    for pd in people_data:
        person = Person()
        populate_person(person, pd)
        person.save()
        created_count += 1

    print("Created {created_count} new users!".format(created_count=created_count))


def get_existing_people_by_myd_person_id():
    existing_people = Person.objects.all()
    existing_people_by_myd_person_id = {p.myd_person_id: p for p in existing_people}
    return existing_people_by_myd_person_id


def get_acny_church_ids():
    cdls = ChurchDataLinker.objects.all()
    acny_church_ids = [cdl.acny_church_id for cdl in cdls]
    return acny_church_ids


def get_myd_people_data(acny_church_ids, db):
    if len(acny_church_ids) == 0:
        return {}
    c = db.cursor(cursorclass=DictCursor)

    # MySQLdb is whacky when using a list of things for "WHERE x IN (x, y, z)"
    # type queries. See here for more information:
    # http://stackoverflow.com/questions/589284/imploding-a-list-for-use-in-a-python-mysqldb-in-clause
    # placeholders = ', '.join(['%s'] * len(acny_church_ids))
    sql = """
SELECT *
FROM (
    SELECT p.PersonID as p_PersonID, p.*
    FROM tblpeople AS p
    INNER JOIN tblpeoplemanager AS pm ON p.PersonID = pm.PersonID
    INNER JOIN tjoinpeopleposition AS pp ON p.PersonID = pp.PersonID
    INNER JOIN tlkpposition AS kp ON pp.PositionID = kp.PositionID
    INNER JOIN tblareaofwork AS aow ON pp.areaofworkid = aow.areaofworkid
    WHERE
        kp.directoryweb = 1 AND
        pm.donotcontact = 0 AND
        p.Deceased != 1 AND
        (
            (p.dpacategoryid = 2 OR p.dpacategoryid IS NULL) OR
            (p.dpacategoryid = 1 AND p.dpastatusid = 1)
        ) AND
        p.Website = 1 AND
        pp.StartDate IS NOT NULL AND
        pp.StartDate < %s AND
        (pp.FinishDate IS NULL OR pp.FinishDate > %s) AND
        (pp.RetireDate IS NULL OR pp.RetireDate > %s)
    ORDER BY p.DateLastEdited DESC
) sub_p
GROUP BY sub_p.p_PersonID;
"""

    c.execute(sql, (timezone.now(), timezone.now(), timezone.now()))

    result_dict = c.fetchallDict()
    all_people_by_person_id = {d['PersonID']: d for d in result_dict}
    return all_people_by_person_id
