import requests
import time

_exchange_cache = None
_exchange_cache_ts = 0

# Используем API с USD как базовой валютой (более стабильный)
EXCHANGE_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'


def get_exchange_rates():
    """Получение актуальных курсов валют с API"""
    global _exchange_cache, _exchange_cache_ts
    ONE_HOUR = 3600
    now = time.time()
    
    if _exchange_cache and (now - _exchange_cache_ts < ONE_HOUR):
        return _exchange_cache
    
    try:
        response = requests.get(EXCHANGE_API_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            _exchange_cache = {
                'USD': 1.0,
                'BYN': rates.get('BYN', 3.2),
                'EUR': rates.get('EUR', 0.92),
                'timestamp': now
            }
            _exchange_cache_ts = now
            print(f"Курсы обновлены: USD=1, BYN={_exchange_cache['BYN']}, EUR={_exchange_cache['EUR']}")
            return _exchange_cache
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
    
    fallback = {
        'USD': 1.0,
        'BYN': 3.2,
        'EUR': 0.92,
        'timestamp': now
    }
    return fallback


def convert_currency(amount_byn, target_currency):
    """Конвертация из BYN в целевую валюту"""
    if not amount_byn:
        return 0
    
    rates = get_exchange_rates()
    amount = float(amount_byn)
    
    # Сначала конвертируем BYN в USD
    usd_amount = amount / rates['BYN']
    
    if target_currency == 'BYN':
        return round(amount, 2)
    elif target_currency == 'USD':
        return round(usd_amount, 2)
    elif target_currency == 'EUR':
        eur_amount = usd_amount * rates['EUR']
        return round(eur_amount, 2)
    else:
        return round(amount, 2)


def get_currency_symbol(currency):
    symbols = {
        'BYN': 'Br',
        'USD': '$',
        'EUR': '€'
    }
    return symbols.get(currency, currency)