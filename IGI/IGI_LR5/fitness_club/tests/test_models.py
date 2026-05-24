import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.users.models import Client, validate_phone, validate_age_18

@pytest.mark.django_db
def test_client_age_validation():
    # 1. Age is exactly 18 -> Valid
    eighteen_years_ago = date.today() - timedelta(days=18 * 365.25)
    validate_age_18(eighteen_years_ago)  # should not raise ValidationError
    
    # 2. Too young (< 18) -> Invalid
    fourteen_years_ago = date.today() - timedelta(days=14 * 365.25)
    with pytest.raises(ValidationError) as excinfo:
        validate_age_18(fourteen_years_ago)
    assert "Возраст клиента должен быть не менее 18 лет." in str(excinfo.value)


@pytest.mark.django_db
def test_client_phone_validation():
    # 1. Correct numbers matching mask -> Valid
    validate_phone("+375 (29) 111-22-33")
    validate_phone("+375 (44) 999-99-99")
    
    # 2. Invalid masks -> raise ValidationError
    invalid_phones = [
        "80291112233",
        "+375294445566",
        "+375 (17) 222-33-44", # incorrect code (17 instead of mobile code)
        "abc-def-gh-ij"
    ]
    for ph in invalid_phones:
        with pytest.raises(ValidationError):
            validate_phone(ph)
