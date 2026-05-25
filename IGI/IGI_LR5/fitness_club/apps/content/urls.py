from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
]