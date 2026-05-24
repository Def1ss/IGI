from django.contrib import admin
from .models import WorkoutType, Group, GroupInstructor, ScheduledClass

@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price_per_session', 'price_per_cycle')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'workout_type')
    search_fields = ('name',)
    list_filter = ('workout_type',)

@admin.register(ScheduledClass)
class ScheduledClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'start_time', 'end_time', 'hall')
    list_filter = ('hall', 'start_time')
    search_fields = ('group__name',)
