from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction

from digitaldiocese.datawrangler.models import ParishDataLinker
from MySQLdb import connect
from MySQLdb.cursors import DictCursor


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_parish_geo()


@transaction.atomic
def update_parish_geo():
    if settings.MYD_DB_HOST is None:
        raise CommandError("MyDiocese DB settings not configured.")
    db = connect(host=settings.MYD_DB_HOST,
                 port=int(settings.MYD_DB_PORT),
                 user=settings.MYD_DB_USERNAME,
                 passwd=settings.MYD_DB_PASSWORD,
                 db=settings.MYD_DB_DATABASE)

    parishes_by_acny_id = get_all_parishes_by_acny_id()
    print("I know about {parish_count} parishes...".format(parish_count=len(parishes_by_acny_id)))

    # get matching myd parish data
    myd_parish_data = get_myd_parish_data(parishes_by_acny_id.keys(), db)
    print("There's {myd_count} matching parishes in MyD...".format(myd_count=len(myd_parish_data)))

    update_parishes(parishes_by_acny_id, myd_parish_data)


def update_parishes(parishes_by_acny_id, myd_parish_data):
    updated = 0
    for data in myd_parish_data:
        acny_id = int(data['CCRef'])
        parish = parishes_by_acny_id[acny_id]
        parish.boundary_data = data['BoundaryData'] or ""
        parish.save()
        updated += 1
    print("Updated {updated} parishes!".format(updated=updated))


def get_all_parishes_by_acny_id():
    pdls = ParishDataLinker.objects.filter(acny_parish_id__isnull=False)
    by_acny_id = {pdl.acny_parish_id: pdl.parish for pdl in pdls}
    return by_acny_id


def get_myd_parish_data(acny_parish_ids, db):
    c = db.cursor(cursorclass=DictCursor)

    # MySQLdb is whacky when using a list of things for "WHERE x IN (x, y, z)"
    # type queries. See here for more information:
    # http://stackoverflow.com/questions/589284/imploding-a-list-for-use-in-a-python-mysqldb-in-clause
    placeholders = ', '.join(['%s'] * len(acny_parish_ids))
    sql = """
SELECT *
FROM tblparish AS p
WHERE p.CCRef in ({placeholders});
""".format(placeholders=placeholders)

    c.execute(sql, (*acny_parish_ids, ))

    result_dict = c.fetchallDict()
    return result_dict
