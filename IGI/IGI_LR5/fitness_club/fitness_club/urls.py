from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.utils import timezone

# API для получения серверного времени
def server_time_api(request):
    """API для получения текущего серверного времени"""
    now_server = timezone.localtime(timezone.now())
    now_utc = timezone.now()
    return JsonResponse({
        'server_local': now_server.strftime('%d.%m.%Y %H:%M:%S'),
        'server_utc': now_utc.strftime('%d.%m.%Y %H:%M:%S'),
        'timestamp': int(now_utc.timestamp()),
    })

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/server-time/', server_time_api, name='server_time_api'),
    
    # Public & client views routed across app namespaces
    path('', include('apps.content.urls')),       # /, /about/, /news/, /faq/, /contacts/, /privacy/, /vacancies/
    path('reviews/', include('apps.reviews.urls')), # /reviews/
    path('promocodes/', include('apps.promocodes.urls')), # /promocodes/
    path('schedule/', include('apps.workouts.urls')), # /schedule/
    path('profile/', include('apps.users.urls')), # /profile/
    path('statistics/', include('apps.analytics.urls')), # /statistics/
    path('individual/sessions/', include('apps.enrollments.urls')), # /individual/sessions/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])