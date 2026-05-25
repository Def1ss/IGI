from django.urls import path

from . import views

app_name = 'content'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('about/', views.AboutView.as_view(), name='about'),

    path('news/', views.NewsListView.as_view(), name='news_list'),

    path(
        'news/<slug:slug>/',
        views.NewsDetailView.as_view(),
        name='news_detail'
    ),

    path('faq/', views.FAQView.as_view(), name='faq'),

    path(
        'contacts/',
        views.ContactsView.as_view(),
        name='contacts'
    ),

    path(
        'vacancies/',
        views.VacancyListView.as_view(),
        name='vacancies'
    ),

    path(
        'privacy/',
        views.PrivacyView.as_view(),
        name='privacy'
    ),

    # =====================================
    # ТЕРМИНЫ
    # =====================================

    path(
        'terms/',
        views.TermListView.as_view(),
        name='term_list'
    ),

    path(
        'terms/create/',
        views.TermCreateView.as_view(),
        name='term_create'
    ),

    path(
        'terms/<int:pk>/',
        views.TermDetailView.as_view(),
        name='term_detail'
    ),

    path(
        'terms/<int:pk>/update/',
        views.TermUpdateView.as_view(),
        name='term_update'
    ),

    path(
        'terms/<int:pk>/delete/',
        views.TermDeleteView.as_view(),
        name='term_delete'
    ),
]