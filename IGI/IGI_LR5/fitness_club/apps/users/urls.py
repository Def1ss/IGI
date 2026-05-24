from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('club-card/purchase/', views.purchase_club_card, name='purchase_club_card'),
    path('currency/', views.set_currency, name='set_currency'),
]
