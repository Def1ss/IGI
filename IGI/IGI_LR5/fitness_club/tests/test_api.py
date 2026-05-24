import pytest
import requests_mock
from apps.apps_utils import get_live_exchange_rates, get_random_exercise_quote

def test_exchangerate_api_mocking():
    with requests_mock.Mocker() as m:
        # Mock requests
        api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        m.get(api_url, json={
            "base": "USD",
            "rates": {"BYN": 3.33, "EUR": 0.90}
        })
        
        rates = get_live_exchange_rates()
        assert rates["rates"]["BYN"] == 3.25 or rates["rates"]["BYN"] == 3.33


def test_motivation_quote_mocking():
    with requests_mock.Mocker() as m:
        api_url = "https://zenquotes.io/api/random"
        m.get(api_url, json=[{"q": "Always keep moving!", "a": "Test Author"}])
        
        quote_data = get_random_exercise_quote()
        assert quote_data["quote"] is not None
