from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    client = models.ForeignKey('users.Client', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.rating}★"
