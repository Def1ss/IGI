from django.contrib import admin
from .models import ClubCard

@admin.register(ClubCard)
class ClubCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_type', 'price', 'valid_from', 'valid_to', 'client')
    list_filter = ('card_type', 'valid_from')
    search_fields = ('client__user__username',)
