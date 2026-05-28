from django.urls import path

from .views import statistics_view

app_name = "analytics"

urlpatterns = [
    path(
        "",
        statistics_view,
        name="statistics",
    ),
]