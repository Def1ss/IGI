from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.enrollments.models import GroupEnrollment
from apps.services import apply_discount, record_promo_usage, sessions_overlap, validate_promo_code
from apps.users.models import Client
from apps.workouts.models import Group, ScheduledClass, WorkoutType


class ScheduleListView(ListView):
    model = ScheduledClass
    template_name = 'workouts/schedule.html'
    context_object_name = 'classes'

    def get_queryset(self):
        qs = (
            ScheduledClass.objects.select_related('group', 'group__workout_type', 'hall')
            .prefetch_related('instructors__user', 'group__enrollments')
            .order_by('start_time')
        )
        date_filter = self.request.GET.get('date')
        group_filter = self.request.GET.get('group')
        hall_filter = self.request.GET.get('hall')
        search = self.request.GET.get('q', '').strip()

        if date_filter:
            qs = qs.filter(start_time__date=date_filter)
        if group_filter:
            qs = qs.filter(group_id=group_filter)
        if hall_filter:
            qs = qs.filter(hall_id=hall_filter)
        if search:
            qs = qs.filter(
                Q(group__name__icontains=search)
                | Q(group__workout_type__name__icontains=search)
                | Q(hall__name__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.select_related('workout_type').all()
        context['halls'] = (
            ScheduledClass.objects.select_related('hall')
            .values_list('hall_id', 'hall__name')
            .distinct()
        )
        context['workout_types'] = WorkoutType.objects.all()
        context['filters'] = {
            'date': self.request.GET.get('date', ''),
            'group': self.request.GET.get('group', ''),
            'hall': self.request.GET.get('hall', ''),
            'q': self.request.GET.get('q', ''),
        }
        client = None
        if self.request.user.is_authenticated:
            client = Client.objects.filter(user=self.request.user).first()
        context['client'] = client
        if client:
            context['enrolled_group_ids'] = set(
                client.enrollments.values_list('group_id', flat=True)
            )
        else:
            context['enrolled_group_ids'] = set()
        return context


@login_required
@require_POST
def enroll_group(request, group_id):
    client = get_object_or_404(Client, user=request.user)
    group = get_object_or_404(Group.objects.select_related('workout_type'), pk=group_id)

    if GroupEnrollment.objects.filter(client=client, group=group).exists():
        messages.error(request, 'Вы уже записаны в эту спортивную группу.')
        return redirect('workouts:schedule')

    new_classes = group.classes.all()
    enrolled_groups = Group.objects.filter(enrollments__client=client)
    existing_classes = ScheduledClass.objects.filter(group__in=enrolled_groups)
    for new_cl in new_classes:
        for existing in existing_classes:
            if sessions_overlap(new_cl.start_time, new_cl.end_time, existing.start_time, existing.end_time):
                messages.error(
                    request,
                    'У вас уже есть другое групповое занятие, которое пересекается с этой группой по времени.',
                )
                return redirect('workouts:schedule')

    wt = group.workout_type
    promo_code = request.POST.get('promo_code', '')
    promo, error = validate_promo_code(promo_code, 'group')
    if error and promo_code:
        messages.error(request, error)
        return redirect('workouts:schedule')

    discount = promo.discount_percent if promo else 0
    final_price = apply_discount(wt.price_per_cycle, discount)

    GroupEnrollment.objects.create(
        client=client,
        group=group,
        paid_amount=final_price,
        payment_status='paid',
    )
    if promo:
        record_promo_usage(promo, client, wt.price_per_cycle, final_price)
    messages.success(request, 'Вы успешно записаны и оплатили цикл групповых занятий.')
    return redirect('workouts:schedule')


@login_required
@require_POST
def bulk_price_increase(request):
    if not request.user.is_superuser:
        messages.error(request, 'Доступ запрещён.')
        return redirect('workouts:schedule')
    workout_type_id = request.POST.get('workout_type_id')
    percent = int(request.POST.get('percent', 10) or 10)
    wt = get_object_or_404(WorkoutType, pk=workout_type_id)
    factor = 1 + percent / 100
    wt.price_per_session = round(float(wt.price_per_session) * factor, 2)
    wt.price_per_cycle = round(float(wt.price_per_cycle) * factor, 2)
    wt.save()
    messages.success(request, f'Цены на «{wt.name}» увеличены на {percent}%.')
    return redirect('workouts:schedule')
