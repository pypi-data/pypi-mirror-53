import re

from django.template.defaulttags import register


@register.filter
def add(value, arg):
    return value + arg


@register.filter
def input_date_format(value):
    if value:
        regex = re.compile('(\d\d)-(\d\d)-(\d\d\d\d)')
        match = re.match(regex, value)

        if match:
            return '{}-{}-{}'.format(match[3], match[2], match[1])
        return value


@register.filter
def input_time_format(value):
    if value:
        regex = re.compile('^(\d\d):(\d\d):(\d\d)$')
        match = re.match(regex, value)

        if match:
            return '{}:{}'.format(match[1], match[2])
        return value


@register.filter
def get(object, key):
    try:
        return object.get(key)
    except:
        return ''


@register.filter
def get_attr(object, key):
    try:
        return getattr(object, key)
    except:
        return ''
