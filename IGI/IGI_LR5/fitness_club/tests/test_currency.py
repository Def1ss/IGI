from apps.apps_utils import convert_from_byn


def test_convert_byn_to_usd():
    rates = {'BYN': 3.25, 'EUR': 0.92, 'USD': 1.0}
    value, code = convert_from_byn(325, 'USD', rates)
    assert code == 'USD'
    assert value == 100.0


def test_convert_byn_stays_byn():
    rates = {'BYN': 3.25, 'EUR': 0.92, 'USD': 1.0}
    value, code = convert_from_byn(50, 'BYN', rates)
    assert code == 'BYN'
    assert value == 50.0
