from datetime import date
from statistics import median

from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.users.models import Client
from apps.workouts.models import WorkoutType
from apps.enrollments.models import (
    GroupEnrollment,
    IndividualSession,
)

from .graph_builders import (
    build_popularity_graph,
    build_revenue_graph,
)


def calculate_age(birth_date):
    today = date.today()
    return (
        today.year
        - birth_date.year
        - (
            (today.month, today.day)
            < (birth_date.month, birth_date.day)
        )
    )


def statistics_view(request):
    clients = []
    ages = []

    for client in Client.objects.select_related("user"):
        age = calculate_age(client.date_of_birth)
        ages.append(age)

        group_paid = (
            GroupEnrollment.objects
            .filter(client=client, payment_status="paid")
            .aggregate(total=Sum("paid_amount"))["total"]
            or 0
        )

        session_paid = (
            IndividualSession.objects
            .filter(client=client, status="completed")
            .aggregate(total=Sum("price"))["total"]
            or 0
        )

        total_paid = group_paid + session_paid

        clients.append({
            "name": client.user.get_full_name() or client.user.username,
            "age": age,
            "total_paid": total_paid,
        })

    avg_age = sum(ages) / len(ages) if ages else 0
    median_age = median(ages) if ages else 0

    sales_values = [float(c["total_paid"]) for c in clients]
    total_sales = sum(sales_values)
    avg_sales = total_sales / len(sales_values) if sales_values else 0
    median_sales = median(sales_values) if sales_values else 0

    # Workout popularity (group only)
    workout_popularity = []
    for wt in WorkoutType.objects.filter(category="group"):
        clients_count = GroupEnrollment.objects.filter(group__workout_type=wt).count()
        workout_popularity.append({
            "name": wt.name,
            "clients_count": clients_count,
        })
    workout_popularity.sort(key=lambda x: x["clients_count"], reverse=True)

    # Workout profit (group + individual)
    workout_profit = []

    for wt in WorkoutType.objects.filter(category="group"):
        profit = (
            GroupEnrollment.objects
            .filter(group__workout_type=wt, payment_status="paid")
            .aggregate(total=Sum("paid_amount"))["total"]
            or 0
        )
        workout_profit.append({
            "name": wt.name,
            "profit": float(profit),
        })

    for wt in WorkoutType.objects.filter(category="individual"):
        profit = (
            IndividualSession.objects
            .filter(workout_type=wt, status="completed")
            .aggregate(total=Sum("price"))["total"]
            or 0
        )
        workout_profit.append({
            "name": wt.name,
            "profit": float(profit),
        })

    workout_profit.sort(key=lambda x: x["profit"], reverse=True)

    # Monthly revenue
    monthly_revenue = []

    group_months = (
        GroupEnrollment.objects
        .filter(payment_status="paid")
        .annotate(month=TruncMonth("enrollment_date"))
        .values("month")
        .annotate(amount=Sum("paid_amount"))
        .order_by("month")
    )

    for item in group_months:
        monthly_revenue.append({
            "month": item["month"].strftime("%m.%Y"),
            "amount": float(item["amount"] or 0),
        })

    session_months = (
        IndividualSession.objects
        .filter(status="completed")
        .annotate(month=TruncMonth("datetime"))
        .values("month")
        .annotate(amount=Sum("price"))
        .order_by("month")
    )

    for item in session_months:
        monthly_revenue.append({
            "month": item["month"].strftime("%m.%Y"),
            "amount": float(item["amount"] or 0),
        })

    monthly_revenue.sort(key=lambda x: x["month"])

    # Build graphs
    popularity_graph = build_popularity_graph(workout_popularity)
    revenue_graph = build_revenue_graph(monthly_revenue)

    total_profit = sum(item["profit"] for item in workout_profit)

    context = {
        "avg_age": avg_age,
        "median_age": median_age,
        "total_sales": total_sales,
        "avg_sales": avg_sales,
        "median_sales": median_sales,
        "clients": clients,
        "workout_popularity": workout_popularity,
        "workout_profit": workout_profit,
        "monthly_revenue": monthly_revenue,
        "total_profit": total_profit,
        "popularity_graph": popularity_graph,
        "revenue_graph": revenue_graph,
    }

    return render(request, "analytics/statistics.html", context)