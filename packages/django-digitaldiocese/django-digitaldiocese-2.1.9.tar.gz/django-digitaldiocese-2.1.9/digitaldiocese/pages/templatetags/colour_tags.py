from django import template

register = template.Library()


NUM_COLOURS = 42


@register.simple_tag
def object_colour(obj, obj_list):
    try:
        index = list(obj_list).index(obj)
        return index % NUM_COLOURS
    except ValueError:
        return 1


@register.filter
def category_colour(counter):
    return counter % NUM_COLOURS
