from django.db import models

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('cardio', 'Кардио'),
        ('strength', 'Силовой'),
        ('functional', 'Функциональный'),
    ]
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    last_maintenance_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class GymHall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    equipment = models.ManyToManyField(
        Equipment, 
        through='HallEquipment', 
        related_name='halls'
    )

    def __str__(self):
        return self.name


class HallEquipment(models.Model):
    hall = models.ForeignKey(GymHall, on_delete=models.CASCADE, related_name='hall_equipments')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='hall_equipments')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hall', 'equipment')

    def __str__(self):
        return f"{self.quantity} x {self.equipment.name} в заде '{self.hall.name}'"
