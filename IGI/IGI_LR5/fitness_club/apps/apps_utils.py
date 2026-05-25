# apps/apps_utils.py
import os
import time
import requests

_exchange_cache = None
_exchange_cache_ts = 0

# Получаем URL из переменных окружения или используем значения по умолчанию
EXCHANGE_RATE_API_URL = os.environ.get('EXCHANGE_RATE_API_URL', 'https://api.exchangerate-api.com/v4/latest/USD')
MOTIVATION_API_URL = os.environ.get('MOTIVATION_API_URL', 'https://zenquotes.io/api/random')


def convert_from_byn(amount_byn, target_currency, rates):
    """Конвертация из BYN в целевую валюту"""
    if target_currency == 'BYN':
        return float(amount_byn), 'BYN'
    
    byn_to_usd = rates.get('BYN', 3.25)
    if target_currency == 'USD':
        result = float(amount_byn) / byn_to_usd
        return round(result, 2), 'USD'
    elif target_currency == 'EUR':
        usd_amount = float(amount_byn) / byn_to_usd
        eur_rate = rates.get('EUR', 0.92)
        result = usd_amount * eur_rate
        return round(result, 2), 'EUR'
    
    return float(amount_byn), 'BYN'


def get_live_exchange_rates():
    global _exchange_cache, _exchange_cache_ts
    ONE_HOUR = 3600
    now = time.time()
    
    if _exchange_cache and (now - _exchange_cache_ts < ONE_HOUR):
        return _exchange_cache
        
    try:
        res = requests.get(EXCHANGE_RATE_API_URL, timeout=5)
        if res.status_code == 200:
            _exchange_cache = res.json()
            _exchange_cache_ts = now
            return _exchange_cache
    except Exception:
        pass
        
    fallback = {
        "base": "USD",
        "rates": {
            "BYN": 3.25,
            "EUR": 0.92,
            "USD": 1.0
        }
    }
    return fallback


def get_random_exercise_quote():
    try:
        res = requests.get(MOTIVATION_API_URL, timeout=3)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                return {
                    "quote": data[0].get("q"),
                    "author": data[0].get("a", "ZenQuotes")
                }
    except Exception:
        pass
        
    return {
        "quote": "Движение — это жизнь, а регулярный фитнес — это здоровая и красивая жизнь!",
        "author": "Фитнес Мотиватор"
    }