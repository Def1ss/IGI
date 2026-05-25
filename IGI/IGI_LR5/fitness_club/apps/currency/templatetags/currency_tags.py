from django import template
from apps.currency.services import convert_currency, get_currency_symbol

register = template.Library()


@register.simple_tag(takes_context=True)
def convert_price(context, amount_byn):
    request = context.get('request')
    if request:
        currency = request.session.get('currency', 'BYN')
    else:
        currency = 'BYN'
    
    converted = convert_currency(amount_byn, currency)
    symbol = get_currency_symbol(currency)
    return f'{converted:.2f} {symbol}'


@register.filter
def currency_symbol(currency_code):
    return get_currency_symbol(currency_code)