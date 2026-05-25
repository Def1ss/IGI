from django import template

from apps.apps_utils import convert_from_byn

register = template.Library()


@register.simple_tag(takes_context=True)
def money(context, amount_byn):
    """Конвертация суммы из BYN в выбранную валюту."""
    rates = context.get('exchange_rates', {})
    currency = context.get('selected_currency', 'BYN')
    value, code = convert_from_byn(amount_byn, currency, rates)
    return f'{value:.2f} {code}'
