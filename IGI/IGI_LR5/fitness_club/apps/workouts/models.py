from django.db import models
from django.core.exceptions import ValidationError

class WorkoutType(models.Model):
    CATEGORIES = [
        ('group', 'Групповое'),
        ('individual', 'Индивидуальное'),
    ]
    name = models.CharField(max_length=150)
    description = models.TextField()
    price_per_session = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price_per_cycle = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.CharField(max_length=15, choices=CATEGORIES)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Group(models.Model):
    name = models.CharField(max_length=150)
    workout_type = models.ForeignKey(
        WorkoutType, 
        on_delete=models.CASCADE, 
        limit_choices_to={'category': 'group'},
        related_name='groups'
    )
    instructors = models.ManyToManyField(
        'users.Instructor', 
        through='GroupInstructor', 
        related_name='groups'
    )
    clients = models.ManyToManyField(
        'users.Client', 
        through='enrollments.GroupEnrollment', 
        related_name='enrolled_groups'
    )

    def __str__(self):
        return self.name


class GroupInstructor(models.Model):
    ROLES = [
        ('main', 'Главный'),
        ('assistant', 'Ассистент'),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_instructors')
    instructor = models.ForeignKey('users.Instructor', on_delete=models.CASCADE, related_name='group_instructors')
    role = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        unique_together = ('group', 'instructor')

    def __str__(self):
        return f"{self.instructor} ({self.get_role_display()}) в {self.group.name}"


class ScheduledClass(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='classes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    hall = models.ForeignKey('gym.GymHall', on_delete=models.CASCADE, related_name='classes')
    instructors = models.ManyToManyField('users.Instructor', related_name='scheduled_classes')

    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("Дата и время окончания занятия не могут быть раньше или тождественно времени начала.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.group.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
