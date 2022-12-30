import datetime
from django import template

register = template.Library()


@register.simple_tag
def tempo_atualf():
    return datetime.datetime.now().strftime('%A  %d %B %Y')

@register.filter(name='range')
def filter_range(start, end):
  return range(start, end)

