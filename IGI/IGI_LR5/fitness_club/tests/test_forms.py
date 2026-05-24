from django import forms
from apps.users.models import Client
from apps.promocodes.models import PromoCode
from apps.enrollments.models import IndividualSession

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['date_of_birth', 'phone', 'address']


def test_client_form_validators():
    # 1. Test invalid phone entry
    form_data = {
        'date_of_birth': '1995-10-10',
        'phone': '12345', # Too short, invalid format
        'address': 'г. Минск, пр-т Победителей 10'
    }
    form = ClientForm(data=form_data)
    assert not form.is_valid()
    assert 'phone' in form.errors
