from django.urls import path

from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.ScheduleListView.as_view(), name='schedule'),
    path('enroll/<int:group_id>/', views.enroll_group, name='enroll_group'),
    path('bulk-price/', views.bulk_price_increase, name='bulk_price'),
]
