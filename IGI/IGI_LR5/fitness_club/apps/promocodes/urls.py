from django.urls import path

from . import views

app_name = 'promocodes'

urlpatterns = [
    path('', views.promo_list, name='list'),
    path('apply/', views.apply_promo, name='apply'),
]
