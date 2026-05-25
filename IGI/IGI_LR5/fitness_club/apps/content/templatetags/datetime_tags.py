# apps/templatetags/datetime_tags.py
from datetime import timezone as datetime_timezone
from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def show_datetime(dt, mode='local'):
    if not dt:
        return '—'
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    
    utc_val = dt.astimezone(datetime_timezone.utc)
    if mode == 'utc':
        shown = utc_val
        label = 'UTC'
    else:
        shown = timezone.localtime(dt)
        label = 'локальное'
    return f'{shown.strftime("%d.%m.%Y %H:%M")} ({label}) / UTC: {utc_val.strftime("%d.%m.%Y %H:%M")}'