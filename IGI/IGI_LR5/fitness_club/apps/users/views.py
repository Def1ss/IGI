from datetime import date, timedelta

from apps.promocodes.services import apply_discount, record_promo_usage, validate_promo_code
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.club_cards.models import ClubCard
from apps.services import apply_discount, record_promo_usage, validate_promo_code
from apps.users.forms import ClientProfileForm, LoginForm, RegisterForm
from apps.users.models import Client, Instructor


def _get_client(user):
    return Client.objects.filter(user=user).select_related('club_card').first()


def _get_instructor(user):
    return Instructor.objects.filter(user=user).first()


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Добро пожаловать!')
        return redirect('users:profile')
    return render(request, 'users/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user, _client = form.save()
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно.')
        return redirect('users:profile')
    return render(request, 'users/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('content:home')


@login_required
def profile_view(request):
    client = _get_client(request.user)
    instructor = _get_instructor(request.user)
    profile_form = None
    if client and request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = ClientProfileForm(request.POST, instance=client)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('users:profile')
    elif client:
        profile_form = ClientProfileForm(instance=client)

    enrollments = []
    club_cards = []
    if client:
        enrollments = client.enrollments.select_related('group', 'group__workout_type').all()
        club_cards = ClubCard.objects.filter(client=client).order_by('-valid_from')

    instructor_sessions = []
    if instructor:
        instructor_sessions = instructor.individual_sessions.select_related(
            'client__user', 'workout_type'
        ).order_by('datetime')

    return render(
        request,
        'users/profile.html',
        {
            'client': client,
            'instructor': instructor,
            'profile_form': profile_form,
            'enrollments': enrollments,
            'club_cards': club_cards,
            'instructor_sessions': instructor_sessions,
            'card_prices': {'trial': 15, 'monthly': 60, 'yearly': 500},
        },
    )


@login_required
@require_POST
def purchase_club_card(request):
    client = _get_client(request.user)
    if not client:
        messages.error(request, 'Покупка доступна только клиентам.')
        return redirect('users:profile')

    card_type = request.POST.get('card_type')
    prices = {'trial': 15, 'monthly': 60, 'yearly': 500}
    if card_type not in prices:
        messages.error(request, 'Неверный тип абонемента.')
        return redirect('users:profile')

    base_price = prices[card_type]
    promo_code = request.POST.get('promo_code', '')
    promo, error = validate_promo_code(promo_code, 'club_card')
    if error and promo_code:
        messages.error(request, error)
        return redirect('users:profile')

    discount = promo.discount_percent if promo else 0
    final_price = apply_discount(base_price, discount)

    valid_from = date.today()
    if card_type == 'trial':
        valid_to = valid_from + timedelta(days=7)
    elif card_type == 'monthly':
        valid_to = valid_from + timedelta(days=30)
    else:
        valid_to = valid_from + timedelta(days=365)

    card = ClubCard.objects.create(
        card_type=card_type,
        price=final_price,
        valid_from=valid_from,
        valid_to=valid_to,
        client=client,
    )
    client.club_card = card
    client.save(update_fields=['club_card'])
    if promo:
        record_promo_usage(promo, client, base_price, final_price)
    messages.success(request, f'Абонемент «{card.get_card_type_display()}» успешно приобретён.')
    return redirect('users:profile')


@require_POST
def set_currency(request):
    currency = request.POST.get('currency', 'BYN')
    if currency in ('BYN', 'USD', 'EUR'):
        request.session['currency'] = currency
        messages.success(request, f'Валюта изменена на {currency}. Курсы обновляются каждый час.')
    else:
        messages.error(request, 'Неверная валюта')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
