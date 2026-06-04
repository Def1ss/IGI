from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    medical_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    specialization = models.CharField(max_length=150)
    hire_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} ({self.specialization})"

class ClubCard(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=50) # 'Standart', 'VIP', 'Family'
    purchase_date = models.DateField(auto_now_add=True)
    valid_to = models.DateField()
    price_paid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Карта {self.card_type} для {self.client}"
