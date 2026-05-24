from django.db import models

class GroupEnrollment(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Оплачено'),
        ('pending', 'Ожидает оплаты'),
    ]
    client = models.ForeignKey('users.Client', on_delete=models.CASCADE, related_name='enrollments')
    group = models.ForeignKey('workouts.Group', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('client', 'group')

    def __str__(self):
        return f"{self.client} ↔ {self.group.name} ({self.get_payment_status_display()})"


class IndividualSession(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('completed', 'Проведено'),
        ('cancelled', 'Отменено'),
    ]
    client = models.ForeignKey('users.Client', on_delete=models.CASCADE, related_name='individual_sessions')
    instructor = models.ForeignKey('users.Instructor', on_delete=models.CASCADE, related_name='individual_sessions')
    workout_type = models.ForeignKey(
        'workouts.WorkoutType', 
        on_delete=models.CASCADE, 
        limit_choices_to={'category': 'individual'},
        related_name='individual_sessions'
    )
    datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')

    def save(self, *args, **kwargs):
        # Auto copy price from WorkoutType price_per_session on creation
        if not self.price and self.workout_type:
            self.price = self.workout_type.price_per_session
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} - {self.instructor} ({self.datetime.strftime('%Y-%m-%d %H:%M')})"
