from django.contrib import admin
from .models import GroupEnrollment, IndividualSession

@admin.register(GroupEnrollment)
class GroupEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'group', 'enrollment_date', 'paid_amount', 'payment_status')
    list_filter = ('payment_status', 'enrollment_date')
    search_fields = ('client__user__username', 'group__name')

@admin.register(IndividualSession)
class IndividualSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'instructor', 'workout_type', 'datetime', 'price', 'status')
    list_filter = ('status', 'datetime')
    search_fields = ('client__user__username', 'instructor__user__username')
