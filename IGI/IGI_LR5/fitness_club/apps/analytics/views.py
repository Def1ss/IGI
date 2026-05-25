# apps/analytics/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from collections import Counter


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser, login_url='/profile/')
def statistics_view(request):
    # Данные клиентов (в алфавитном порядке)
    clients_data = [
        {'name': 'Александр Петров', 'age': 29, 'total_paid': 1250},
        {'name': 'Анна Соколова', 'age': 22, 'total_paid': 890},
        {'name': 'Артем Кузнецов', 'age': 27, 'total_paid': 1500},
        {'name': 'Денис Кравченко', 'age': 34, 'total_paid': 2100},
        {'name': 'Екатерина Морозова', 'age': 24, 'total_paid': 950},
        {'name': 'Мария Ковалева', 'age': 26, 'total_paid': 1100},
        {'name': 'Максим Попов', 'age': 39, 'total_paid': 3200},
        {'name': 'Сергей Федоров', 'age': 36, 'total_paid': 2800},
        {'name': 'Юлия Рыбакова', 'age': 31, 'total_paid': 1700},
        {'name': 'Владислав Тарасов', 'age': 33, 'total_paid': 1950},
    ]
    
    # Сортируем по имени
    clients_sorted = sorted(clients_data, key=lambda x: x['name'])
    
    # 1. Общая сумма продаж
    total_sales = sum(c['total_paid'] for c in clients_data)
    
    # 2. Среднее, мода, медиана по сумме продаж
    sales = [c['total_paid'] for c in clients_data]
    avg_sales = round(sum(sales) / len(sales), 2)
    
    # Мода (самое частое значение)
    freq = Counter(sales)
    mode_sales = max(freq, key=lambda x: freq[x]) if freq else 0
    
    # Медиана
    sorted_sales = sorted(sales)
    n = len(sorted_sales)
    if n % 2 == 0:
        median_sales = (sorted_sales[n//2 - 1] + sorted_sales[n//2]) / 2
    else:
        median_sales = sorted_sales[n//2]
    
    # 3. Средний и медианный возраст клиентов
    ages = [c['age'] for c in clients_data]
    avg_age = round(sum(ages) / len(ages), 1)
    
    sorted_ages = sorted(ages)
    if n % 2 == 0:
        median_age = (sorted_ages[n//2 - 1] + sorted_ages[n//2]) / 2
    else:
        median_age = sorted_ages[n//2]
    
    # 4. Популярность типов тренировок
    workout_popularity = [
        {'name': 'Кроссфит', 'clients_count': 45},
        {'name': 'Йога', 'clients_count': 38},
        {'name': 'Пилатес', 'clients_count': 32},
        {'name': 'Кардио', 'clients_count': 28},
        {'name': 'Индивидуальные', 'clients_count': 25},
    ]
    
    # Сортируем по популярности
    most_popular = sorted(workout_popularity, key=lambda x: x['clients_count'], reverse=True)
    
    # 5. Прибыльность типов тренировок
    workout_profit = [
        {'name': 'Кроссфит', 'profit': 24500},
        {'name': 'Йога', 'profit': 18900},
        {'name': 'Пилатес', 'profit': 15600},
        {'name': 'Индивидуальные', 'profit': 34200},
        {'name': 'Кардио', 'profit': 9800},
    ]
    
    most_profitable = sorted(workout_profit, key=lambda x: x['profit'], reverse=True)
    
    # ВЫЧИСЛЯЕМ ОБЩУЮ ПРИБЫЛЬ (вот это нужно добавить)
    total_profit = sum(item['profit'] for item in workout_profit)
    
    # 6. Данные для графика по месяцам
    monthly_revenue = [
        {'month': 'Январь', 'amount': 12500},
        {'month': 'Февраль', 'amount': 14800},
        {'month': 'Март', 'amount': 16200},
        {'month': 'Апрель', 'amount': 18900},
        {'month': 'Май', 'amount': 21000},
        {'month': 'Июнь', 'amount': 23500},
    ]
    
    # ВЫЧИСЛЯЕМ ОБЩИЙ ДОХОД ЗА 6 МЕСЯЦЕВ (тоже можно добавить)
    total_revenue = sum(item['amount'] for item in monthly_revenue)
    
    context = {
        'clients': clients_sorted,
        'total_sales': total_sales,
        'avg_sales': avg_sales,
        'mode_sales': mode_sales,
        'median_sales': median_sales,
        'avg_age': avg_age,
        'median_age': median_age,
        'workout_popularity': most_popular,
        'workout_profit': most_profitable,
        'monthly_revenue': monthly_revenue,
        'total_profit': total_profit,      # ДОБАВИТЬ ЭТУ СТРОКУ
        'total_revenue': total_revenue,    # ДОБАВИТЬ ЭТУ СТРОКУ (опционально)
    }
    
    return render(request, 'analytics/statistics.html', context)