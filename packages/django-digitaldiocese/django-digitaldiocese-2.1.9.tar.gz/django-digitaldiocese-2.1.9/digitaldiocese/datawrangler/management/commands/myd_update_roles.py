from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction

from digitaldiocese.acny.models import ChurchRole, Person
from digitaldiocese.datawrangler.models import ChurchDataLinker
from MySQLdb import connect
from MySQLdb.cursors import DictCursor


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_myd_roles()


def update_myd_roles():
    if settings.MYD_DB_HOST is None:
        raise CommandError("MyDiocese DB settings not configured.")
    db = connect(host=settings.MYD_DB_HOST,
                 port=int(settings.MYD_DB_PORT),
                 user=settings.MYD_DB_USERNAME,
                 passwd=settings.MYD_DB_PASSWORD,
                 db=settings.MYD_DB_DATABASE,
                 )

    # get all church ids
    churches_by_church_id = get_churches_by_acny_church_id()
    print("I know about {church_count} church IDs...".format(
        church_count=len(churches_by_church_id)
    ))

    # get all myd positions
    myd_positions_by_tjppid = get_myd_position_data(churches_by_church_id.keys(), db)
    print("There's data on {position_count} positions in MyD...".format(
        position_count=len(myd_positions_by_tjppid)))

    # get all roles in system
    roles_by_tjppid = get_all_roles_by_tjppid()
    print("There's {role_count} roles in the system...".format(role_count=len(roles_by_tjppid)))

    # get all people in system
    people_by_people_id = get_existing_people_by_myd_person_id()
    print("There's currently {existing_count} people in the system...".format(
        existing_count=len(people_by_people_id)))

    add_new_roles(
        myd_positions_by_tjppid, roles_by_tjppid, people_by_people_id, churches_by_church_id
    )

    update_roles(
        myd_positions_by_tjppid, roles_by_tjppid, people_by_people_id, churches_by_church_id
    )

    delete_roles(
        myd_positions_by_tjppid, roles_by_tjppid, people_by_people_id, churches_by_church_id
    )


@transaction.atomic
def add_new_roles(myd_p_by_tjppid, roles_by_tjppid, people_by_people_id, churches_by_church_id):
    to_add = list(set(myd_p_by_tjppid.keys()) - set(roles_by_tjppid.keys()))
    print("Will add {add_count} new roles...".format(add_count=len(to_add)))

    created = 0
    for tjppid in to_add:
        data = myd_p_by_tjppid[tjppid]
        try:
            person = people_by_people_id[data['PersonID']]
        except KeyError:
            continue

        if data['ccref'] is not None:
            try:
                for church in churches_by_church_id[data['ccref']]:
                    role = populate_role(ChurchRole(), data, person, church)
            except KeyError:
                continue
        else:
            role = populate_role(ChurchRole(), data, person, church=None)

        role.save()
        created += 1

    print("Created {created} new roles!".format(created=created))


@transaction.atomic
def update_roles(myd_p_by_tjppid, roles_by_tjppid, people_by_people_id, churches_by_church_id):
    updated_venues = 0
    updated_roles = 0
    for tjppid, data in myd_p_by_tjppid.items():
        try:
            role = roles_by_tjppid[tjppid]
        except KeyError:
            # brand new roles won't be in this dict
            continue

        person = people_by_people_id[data['PersonID']]
        if data['ccref'] is not None:
            for church in churches_by_church_id[data['ccref']]:
                role = populate_role(role, data, person, church)
                updated_venues += 1
        else:
            role = populate_role(role, data, person, church=None)
        role.save()
        updated_roles += 1

    print("Updated roles for {updated_venues} venues with {updated_roles} roles!".format(
        updated_venues=updated_venues, updated_roles=updated_roles))


def delete_roles(myd_p_by_tjppid, roles_by_tjppid, people_by_people_id, churches_by_church_id):
    to_delete = list(set(set(roles_by_tjppid.keys() - myd_p_by_tjppid.keys())))
    ChurchRole.objects.filter(myd_tjppid__in=to_delete).delete()
    print("Deleted {delete_count} roles!".format(delete_count=len(to_delete)))


def populate_role(role, data, person, church):
    role.person = person
    role.church = church
    role.myd_tjppid = data['tjppid']
    if data['PositionDescription'] is not None:
        role.role_name = data['PositionDescription']
    else:
        role.role_name = ""
    return role


def get_existing_people_by_myd_person_id():
    existing_people = Person.objects.all()
    existing_people_by_myd_person_id = {p.myd_person_id: p for p in existing_people}
    return existing_people_by_myd_person_id


def get_all_roles_by_tjppid():
    church_roles = ChurchRole.objects.filter(myd_tjppid__isnull=False)
    by_tjppid = {cr.myd_tjppid: cr for cr in church_roles}
    return by_tjppid


def get_churches_by_acny_church_id():
    cdls = ChurchDataLinker.objects.all()

    by_acny_id = {}
    for cdl in cdls:
        church_id = cdl.acny_church_id
        if church_id not in by_acny_id:
            by_acny_id[church_id] = []
        by_acny_id[church_id].append(cdl.venue_data_linker.church)
    return by_acny_id


def get_myd_position_data(acny_church_ids, db):
    c = db.cursor(cursorclass=DictCursor)

    sql = """
SELECT *
FROM tblpeople AS p
INNER JOIN tblpeoplemanager AS pm ON p.PersonID = pm.PersonID
INNER JOIN tjoinpeopleposition AS pp ON p.PersonID = pp.PersonID
INNER JOIN tlkpposition AS kp ON pp.PositionID = kp.PositionID
INNER JOIN tblareaofwork AS aow
    ON pp.areaofworkid = aow.areaofworkid
LEFT JOIN tblchurch c ON aow.areaofworkid = c.areaofworkid
WHERE
    kp.directoryweb = 1 AND
    (
        (pp.StartDate < NOW() OR pp.StartDate IS NULL) AND
        (pp.FinishDate > NOW() OR pp.FinishDate IS NULL)
    )
GROUP BY pp.tjppid;"""

    c.execute(sql)

    result_dict = c.fetchallDict()
    all_positions_by_tjppid = {d['tjppid']: d for d in result_dict}
    return all_positions_by_tjppid
