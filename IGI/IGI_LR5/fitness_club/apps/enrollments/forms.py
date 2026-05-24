from django import forms

from apps.enrollments.models import IndividualSession
from apps.users.models import Instructor
from apps.workouts.models import WorkoutType


class BookSessionForm(forms.Form):
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.select_related('user'),
        label='Тренер',
    )
    workout_type = forms.ModelChoiceField(
        queryset=WorkoutType.objects.filter(category='individual'),
        label='Вид тренировки',
    )
    datetime = forms.DateTimeField(
        label='Дата и время',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    duration_minutes = forms.IntegerField(
        min_value=30,
        max_value=180,
        initial=60,
        label='Длительность (мин)',
    )
    promo_code = forms.CharField(required=False, label='Промокод')
