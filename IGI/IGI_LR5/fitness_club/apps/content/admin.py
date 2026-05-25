from django.contrib import admin
from .models import News, Vacancy, FAQ, ContactPerson, CompanyHistory

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_date', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'full_text')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('position', 'salary', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('position',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'added_date')
    search_fields = ('question', 'answer')

@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'role', 'phone', 'email')
    search_fields = ('full_name', 'role')

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'event')
    ordering = ('year',)
