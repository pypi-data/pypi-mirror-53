from collections import OrderedDict

from django import template
from django.utils import timezone

from ..forms import PostcodeForm

register = template.Library()


@register.assignment_tag
def get_acny_form():
    return PostcodeForm()


@register.assignment_tag
def sort_by_role_name(roles, *sort_order_role_names):
    """
    Takes an iterable of roles, and orders them by the supplied list of role names. Any remaining
    roles are appended to the end, unsorted.
    """
    sort_order_role_names = [role_name.lower() for role_name in sort_order_role_names]

    sort_key = SortRolesByRoleName(sort_order_role_names)
    return sorted(roles, key=sort_key)


class SortRolesByRoleName(object):
    """
    A utility class to sort a list of roles by their role name.

    Blame @martinphellwig ;)
    """
    def __init__(self, sort_order_role_names):
        self.sort_order_role_names = sort_order_role_names

    def __call__(self, role):
        role_name = role.role_name.lower()

        if role_name in self.sort_order_role_names:
            index = self.sort_order_role_names.index(role_name)
        else:
            index = len(self.sort_order_role_names)

        sort_by = str(index) + ':' + role.role_name.lower()
        return sort_by


@register.assignment_tag
def get_services(church):
    regular_services = OrderedDict()
    other_events = []
    returns = {
        'regular_services': False,
        'other_events': False
    }

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    map_attribute_day = {}
    by_week_empty = True

    now = timezone.now().date()

    for day in days:
        regular_services[day] = []
        # For now the attributes are straight forward mapped, but I can imagine
        # that the day of week strings at some point need to be localised since
        # they are directly used in the template as a value.
        map_attribute_day[day.lower()] = day

    for service in church.services.all().order_by('time'):
        if service.recurring:
            # These services are recurring on a weekly basis.
            on_days = service.get_days()
            if len(on_days) != 0 and by_week_empty:
                by_week_empty = False

            for attribute_name in service.get_days():
                regular_services[map_attribute_day[attribute_name]].append(service)
        else:
            # These are 'other' events.
            if service.date and service.date > now:
                other_events.append(service)

    if not by_week_empty:
        returns['regular_services'] = regular_services

    if other_events:
        returns['other_events'] = other_events
        returns['other_events'].sort(key=lambda item: [item.date, item.time])

    return returns
