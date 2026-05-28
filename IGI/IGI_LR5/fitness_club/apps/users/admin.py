from collections import Counter
from statistics import mean, median, mode, StatisticsError
from datetime import date

from django.contrib import admin
from django.db.models import Sum
from django.template.response import TemplateResponse
from django.urls import path

from .models import Client, Instructor
from apps.enrollments.models import GroupEnrollment, IndividualSession
from apps.workouts.models import GroupInstructor
from apps.club_cards.models import ClubCard


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
    list_display = (
        'id',
        'user',
        'phone',
        'date_of_birth',
        'club_card',
        'registration_date'
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone'
    )

    list_filter = (
        'registration_date',
        'club_card__card_type'
    )

    inlines = [GroupEnrollmentInline]

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                'statistics/',
                self.admin_site.admin_view(self.statistics_view),
                name='client-statistics',
            ),
        ]

        return custom_urls + urls

    def statistics_view(self, request):
        clients = Client.objects.select_related(
            'user',
            'club_card'
        ).order_by('user__username')

        cards = ClubCard.objects.all()

        # =========================
        # Общая прибыль
        # =========================

        total_sales = (
            cards.aggregate(total=Sum('price'))['total']
            or 0
        )

        # =========================
        # Возрасты клиентов
        # =========================

        ages = []

        today = date.today()

        for client in clients:
            age = (
                today.year
                - client.date_of_birth.year
                - (
                    (today.month, today.day)
                    <
                    (
                        client.date_of_birth.month,
                        client.date_of_birth.day
                    )
                )
            )

            ages.append(age)

        avg_age = round(mean(ages), 2) if ages else 0
        median_age = median(ages) if ages else 0

        # =========================
        # Продажи
        # =========================

        prices = [float(card.price) for card in cards]

        avg_sales = round(mean(prices), 2) if prices else 0
        median_sales = median(prices) if prices else 0

        try:
            sales_mode = mode(prices) if prices else 0
        except StatisticsError:
            sales_mode = 'Нет моды'

        # =========================
        # Популярный тип карты
        # =========================

        card_types = [
            card.card_type
            for card in cards
        ]

        most_popular_card = (
            Counter(card_types).most_common(1)[0][0]
            if card_types else 'Нет данных'
        )

        # =========================
        # Самая прибыльная карта
        # =========================

        profit_by_type = {}

        for card in cards:
            profit_by_type.setdefault(card.card_type, 0)
            profit_by_type[card.card_type] += float(card.price)

        most_profitable = (
            max(
                profit_by_type,
                key=profit_by_type.get
            )
            if profit_by_type else 'Нет данных'
        )

        context = dict(
            self.admin_site.each_context(request),

            clients=clients,

            total_sales=total_sales,

            avg_age=avg_age,
            median_age=median_age,

            avg_sales=avg_sales,
            median_sales=median_sales,
            sales_mode=sales_mode,

            most_popular_card=most_popular_card,
            most_profitable=most_profitable,

            title='Статистика фитнес-клуба'
        )

        return TemplateResponse(
            request,
            'admin/statistics.html',
            context
        )


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'experience_years',
        'hire_date'
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name'
    )

    list_filter = (
        'hire_date',
        'specialization'
    )

    inlines = [
        GroupInstructorInline,
        IndividualSessionInline
    ]