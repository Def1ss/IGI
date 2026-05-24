import json
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count, Avg
from apps.users.models import Client
from apps.enrollments.models import GroupEnrollment, IndividualSession
from apps.club_cards.models import ClubCard
from apps.workouts.models import Group, WorkoutType
from django.utils import timezone

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='/profile/')
def statistics_view(request):
    # 1. Classes per groups (Group Name -> class count)
    groups_qs = Group.objects.annotate(classes_count=Count('classes')).values('name', 'classes_count')
    chart_groups_data = {item['name']: item['classes_count'] for item in groups_qs}

    # 2. Avg & Median Age calculations
    clients = Client.objects.all()
    ages = []
    today = timezone.now().date()
    for client in clients:
        dob = client.date_of_birth
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        ages.append(age)
    
    avg_age = sum(ages) / len(ages) if ages else 0
    
    sorted_ages = sorted(ages)
    n = len(sorted_ages)
    if n == 0:
        median_age = 0
    elif n % 2 != 0:
        median_age = sorted_ages[n // 2]
    else:
        median_age = (sorted_ages[n // 2 - 1] + sorted_ages[n // 2]) / 2.0

    # 3. Most Popular Workout Type (By unique clients in groups + individual sessions)
    workout_popularity = {}
    workout_types = WorkoutType.objects.all()
    
    for wt in workout_types:
        unique_clients = set()
        if wt.category == 'group':
            for group in wt.groups.all():
                for enrollment in group.enrollments.all():
                    unique_clients.add(enrollment.client_id)
        else:
            for session in wt.individual_sessions.exclude(status='cancelled'):
                unique_clients.add(session.client_id)
        
        workout_popularity[wt.name] = len(unique_clients)
    
    sorted_popularity = sorted(workout_popularity.items(), key=lambda x: x[1], reverse=True)

    # 4. Highest Profitability category
    workout_profit = {}
    for wt in workout_types:
        profit = 0
        if wt.category == 'group':
            for group in wt.groups.all():
                enrollments_sum = group.enrollments.filter(payment_status='paid').aggregate(total=Sum('paid_amount'))['total']
                if enrollments_sum:
                    profit += enrollments_sum
        else:
            sessions_sum = wt.individual_sessions.filter(status='completed').aggregate(total=Sum('price'))['total']
            if sessions_sum:
                profit += sessions_sum
        workout_profit[wt.name] = float(profit)
        
    sorted_profitability = sorted(workout_profit.items(), key=lambda x: x[1], reverse=True)

    # 5. Clients alphabetical payment lists (cycles + sessions + cards)
    client_payment_list = []
    all_clients = Client.objects.select_related('user').order_by('user__last_name', 'user__first_name')
    for cl in all_clients:
        grp_sum = cl.enrollments.filter(payment_status='paid').aggregate(total=Sum('paid_amount'))['total'] or 0
        ind_sum = cl.individual_sessions.filter(status='completed').aggregate(total=Sum('price'))['total'] or 0
        card_sum = ClubCard.objects.filter(client=cl).aggregate(total=Sum('price'))['total'] or 0
        
        total_spent = grp_sum + ind_sum + card_sum
        client_payment_list.append({
            'full_name': cl.user.get_full_name() or cl.user.username,
            'phone': cl.phone,
            'group_paid': float(grp_sum),
            'individual_paid': float(ind_sum),
            'subscription_paid': float(card_sum),
            'total_paid': float(total_spent)
        })

    # 6. Revenue grouped by month (Simulated summary trends for ChartJS rendering)
    revenue_chart_data = [
        {"month": "Январь", "amount": 1400},
        {"month": "Февраль", "amount": 1850},
        {"month": "Март", "amount": 2500},
        {"month": "Апрель", "amount": 3200},
        {"month": "Май", "amount": 4180}
    ]

    context = {
        'chart_groups_data_json': json.dumps(chart_groups_data),
        'revenue_chart_data_json': json.dumps(revenue_chart_data),
        'avg_age': round(avg_age, 1),
        'median_age': median_age,
        'popularity_list': sorted_popularity,
        'profitability_list': sorted_profitability,
        'client_payments': client_payment_list,
    }
    
    return render(request, 'analytics/statistics.html', context)
