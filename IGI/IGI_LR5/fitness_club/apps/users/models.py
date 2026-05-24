import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_phone(value):
    pattern = r"^\+375\s?\((25|29|33|44)\)\s?[0-9]{3}-[0-9]{2}-[0-9]{2}$"
    if not re.match(pattern, value):
        raise ValidationError("Неверный формат телефона. Требуется: +375 (29) XXX-XX-XX")

def validate_age_18(value):
    today = timezone.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Возраст клиента должен быть не менее 18 лет.")


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    date_of_birth = models.DateField(validators=[validate_age_18])
    phone = models.CharField(max_length=25, validators=[validate_phone])
    address = models.TextField()
    registration_date = models.DateField(auto_now_add=True)
    club_card = models.ForeignKey(
        'club_cards.ClubCard', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='owners'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    specialization = models.ManyToManyField('workouts.WorkoutType', related_name='instructors')
    experience_years = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='instructors/', null=True, blank=True)
    hire_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name() or self.user.username
