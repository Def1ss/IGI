from django.urls import path

from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('<int:session_id>/cancel/', views.cancel_session, name='cancel_session'),
    path('<int:session_id>/complete/', views.complete_session, name='complete_session'),
]
