from django.contrib import admin
from .models import GymHall, Equipment, HallEquipment

class HallEquipmentInline(admin.TabularInline):
    model = HallEquipment
    extra = 1

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'last_maintenance_date')
    list_filter = ('type', 'last_maintenance_date')
    search_fields = ('name',)

@admin.register(GymHall)
class GymHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity')
    search_fields = ('name',)
    inlines = [HallEquipmentInline]
