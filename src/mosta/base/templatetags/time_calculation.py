from django import template

register = template.Library()


@register.filter(name='seconds_to_minutes')
def seconds_to_minutes(seconds: int):
    minutes = seconds / 60
    return '{:02d}:{:02d}'.format(int(minutes), int(seconds % 60))
