# fitness_club/context_processors.py
from django.utils import timezone

# Исправьте импорт - должно быть apps.apps_utils, не apps_utils
from apps.apps_utils import get_live_exchange_rates, get_random_exercise_quote


def site_globals(request):
    rates_data = get_live_exchange_rates()
    rates = rates_data.get('rates', {'BYN': 3.25, 'EUR': 0.92, 'USD': 1.0})
    currency = request.session.get('currency', 'BYN')
    if currency not in ('BYN', 'USD', 'EUR'):
        currency = 'BYN'
    return {
        'exchange_rates': rates,
        'selected_currency': currency,
        'motivation': get_random_exercise_quote(),
        'server_now': timezone.now(),
    }