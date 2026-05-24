import time
import requests

# 1-Hour Cash Core Exchange calculations
_exchange_cache = None
_exchange_cache_ts = 0

def get_live_exchange_rates():
    global _exchange_cache, _exchange_cache_ts
    ONE_HOUR = 3600
    now = time.time()
    
    if _exchange_cache and (now - _exchange_cache_ts < ONE_HOUR):
        return _exchange_cache
        
    try:
        # Fetch actual USD based ratios exchange
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        if res.status_code == 200:
            _exchange_cache = res.json()
            _exchange_cache_ts = now
            return _exchange_cache
    except Exception:
        pass
        
    # Standard robust cache failover
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
    # Fetch random motivational quote from external API
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=3)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                return {
                    "quote": data[0].get("q"),
                    "author": data[0].get("a", "ZenQuotes")
                }
    except Exception:
        pass
        
    # Fallback quotes
    return {
        "quote": "Движение — это жизнь, а регулярный фитнес — это здоровая и красивая жизнь!",
        "author": "Фитнес Мотиватор"
    }
