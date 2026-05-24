from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.enrollments.models import GroupEnrollment, IndividualSession
from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review
from apps.users.models import Client


def _client_can_review(client):
    has_group = GroupEnrollment.objects.filter(client=client, payment_status='paid').exists()
    has_individual = IndividualSession.objects.filter(client=client, status='completed').exists()
    return has_group or has_individual


@require_http_methods(['GET', 'POST'])
def review_list(request):
    reviews = Review.objects.select_related('client__user').order_by('-created_at')
    form = None
    client = None
    if request.user.is_authenticated:
        client = Client.objects.filter(user=request.user).first()
    if client and _client_can_review(client):
        form = ReviewForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            review = form.save(commit=False)
            review.client = client
            review.save()
            messages.success(request, 'Спасибо за отзыв!')
            return redirect('reviews:list')
    elif request.method == 'POST' and request.user.is_authenticated:
        messages.error(
            request,
            'Оставить отзыв могут только клиенты с оплаченным групповым или завершённым индивидуальным занятием.',
        )
    return render(request, 'reviews/list.html', {'reviews': reviews, 'form': form, 'client': client})
