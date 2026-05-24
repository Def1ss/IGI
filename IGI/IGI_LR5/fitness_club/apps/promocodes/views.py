from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.promocodes.models import PromoCode
from apps.services import validate_promo_code


@require_http_methods(['GET'])
def promo_list(request):
    promos = PromoCode.objects.filter(is_active=True).order_by('-valid_from')
    return render(request, 'promocodes/list.html', {'promos': promos})


@require_POST
def apply_promo(request):
    code = request.POST.get('code', '')
    service_type = request.POST.get('service_type', 'all')
    promo, error = validate_promo_code(code, service_type)
    if error:
        messages.error(request, error)
    else:
        request.session['applied_promo'] = {
            'code': promo.code,
            'discount_percent': promo.discount_percent,
            'applicable_to': promo.applicable_to,
        }
        messages.success(request, f'Промокод {promo.code} применён: скидка {promo.discount_percent}%.')
    return redirect(request.META.get('HTTP_REFERER', 'promocodes:list'))
