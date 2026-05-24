from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from apps.enrollments.forms import BookSessionForm
from apps.enrollments.models import IndividualSession
from apps.services import apply_discount, record_promo_usage, sessions_overlap, validate_promo_code
from apps.users.models import Client, Instructor


@login_required
@require_http_methods(['GET', 'POST'])
def session_list(request):
    client = Client.objects.filter(user=request.user).first()
    instructor = Instructor.objects.filter(user=request.user).first()

    if client:
        sessions = client.individual_sessions.select_related(
            'instructor__user', 'workout_type'
        ).order_by('datetime')
    elif instructor:
        sessions = instructor.individual_sessions.select_related(
            'client__user', 'workout_type'
        ).order_by('datetime')
    elif request.user.is_superuser:
        sessions = IndividualSession.objects.select_related(
            'client__user', 'instructor__user', 'workout_type'
        ).order_by('datetime')
    else:
        messages.error(request, 'Раздел доступен клиентам, тренерам и администраторам.')
        return redirect('content:home')

    book_form = None
    if client:
        book_form = BookSessionForm(request.POST or None)
        if request.method == 'POST' and 'book_session' in request.POST and book_form.is_valid():
            data = book_form.cleaned_data
            wt = data['workout_type']
            inst = data['instructor']
            start = data['datetime']
            if timezone.is_naive(start):
                start = timezone.make_aware(start)
            end = start + timedelta(minutes=data['duration_minutes'])

            overlapping = IndividualSession.objects.exclude(status='cancelled').filter(
                datetime__lt=end,
            )
            for session in overlapping:
                s_end = session.datetime + timedelta(minutes=session.duration_minutes)
                if not sessions_overlap(start, end, session.datetime, s_end):
                    continue
                if session.instructor_id == inst.id or session.client_id == client.id:
                    messages.error(
                        request,
                        'У тренера или у вас уже есть запланированное занятие на это время.',
                    )
                    return redirect('enrollments:session_list')

            promo_code = data.get('promo_code', '')
            promo, error = validate_promo_code(promo_code, 'individual')
            if error and promo_code:
                messages.error(request, error)
                return redirect('enrollments:session_list')

            discount = promo.discount_percent if promo else 0
            final_price = apply_discount(wt.price_per_session, discount)

            IndividualSession.objects.create(
                client=client,
                instructor=inst,
                workout_type=wt,
                datetime=start,
                duration_minutes=data['duration_minutes'],
                price=final_price,
                status='scheduled',
            )
            if promo:
                record_promo_usage(promo, client, wt.price_per_session, final_price)
            messages.success(request, 'Индивидуальная тренировка успешно забронирована.')
            return redirect('enrollments:session_list')

    return render(
        request,
        'enrollments/sessions.html',
        {
            'sessions': sessions,
            'book_form': book_form,
            'client': client,
            'instructor': instructor,
        },
    )


@login_required
@require_POST
def cancel_session(request, session_id):
    session = get_object_or_404(IndividualSession, pk=session_id)
    client = Client.objects.filter(user=request.user).first()
    if not client or session.client_id != client.id:
        messages.error(request, 'Отменить может только владелец записи.')
        return redirect('enrollments:session_list')

    hours_left = (session.datetime - timezone.now()).total_seconds() / 3600
    if hours_left < 12:
        messages.error(
            request,
            'Отмена невозможна: до занятия осталось менее 12 часов.',
        )
        return redirect('enrollments:session_list')

    session.status = 'cancelled'
    session.save(update_fields=['status'])
    messages.success(request, 'Запись на тренировку отменена.')
    return redirect('enrollments:session_list')


@login_required
@require_POST
def complete_session(request, session_id):
    session = get_object_or_404(IndividualSession, pk=session_id)
    instructor = Instructor.objects.filter(user=request.user).first()
    if not instructor or session.instructor_id != instructor.id:
        messages.error(request, 'Завершить занятие может только назначенный тренер.')
        return redirect('enrollments:session_list')

    session.status = 'completed'
    session.save(update_fields=['status'])
    messages.success(request, 'Занятие отмечено как проведённое.')
    return redirect('enrollments:session_list')
