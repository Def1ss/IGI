from django.contrib import admin
from .models import Client, Instructor
from apps.enrollments.models import GroupEnrollment, IndividualSession
from apps.workouts.models import GroupInstructor

class GroupEnrollmentInline(admin.TabularInline):
    model = GroupEnrollment
    extra = 1

class IndividualSessionInline(admin.TabularInline):
    model = IndividualSession
    fk_name = 'instructor'
    extra = 1

class GroupInstructorInline(admin.TabularInline):
    model = GroupInstructor
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'date_of_birth', 'club_card', 'registration_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('registration_date', 'club_card__card_type')
    inlines = [GroupEnrollmentInline]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'experience_years', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('hire_date', 'specialization')
    inlines = [GroupInstructorInline, IndividualSessionInline]
