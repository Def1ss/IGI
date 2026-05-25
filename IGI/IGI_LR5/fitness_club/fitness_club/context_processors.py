# fitness_club/context_processors.py
from django.utils import timezone
from apps.currency.services import get_exchange_rates, convert_currency, get_currency_symbol
from apps.apps_utils import get_random_exercise_quote


def site_globals(request):
    # Получаем выбранную валюту из сессии
    selected_currency = request.session.get('currency', 'BYN')
    if selected_currency not in ('BYN', 'USD', 'EUR'):
        selected_currency = 'BYN'
    
    # Получаем курсы валют
    rates = get_exchange_rates()
    
    # Конвертируем пример 100 BYN для отображения
    example_usd = convert_currency(100, 'USD')
    example_eur = convert_currency(100, 'EUR')
    
    return {
        'exchange_rates': rates,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency),
        'motivation': get_random_exercise_quote(),
        'server_now': timezone.localtime(timezone.now()),
        'example_conversion': f"100 BYN ≈ {example_usd} USD / {example_eur} EUR",
    }