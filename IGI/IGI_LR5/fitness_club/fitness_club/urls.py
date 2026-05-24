from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
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
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
