from django.db import models

class ClubCard(models.Model):
    CARD_TYPES = [
        ('trial', 'Пробный (7 дней)'),
        ('monthly', 'Месячный'),
        ('yearly', 'Годовой'),
    ]
    card_type = models.CharField(max_length=15, choices=CARD_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    client = models.ForeignKey(
        'users.Client', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='club_cards_owned'
    )

    def __str__(self):
        return f"{self.get_card_type_display()} - {self.price} BYN"
