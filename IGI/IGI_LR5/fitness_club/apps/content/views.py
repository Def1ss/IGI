from django.views.generic import ListView, DetailView, TemplateView
from .models import News, CompanyHistory, FAQ, ContactPerson, Vacancy
from django.utils.text import slugify
from unidecode import unidecode
from apps.apps_utils import get_random_exercise_quote

class HomeView(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.objects.order_by('-published_date').first()
        context['motivation'] = get_random_exercise_quote()
        return context


class AboutView(ListView):
    model = CompanyHistory
    template_name = 'content/about.html'
    context_object_name = 'history_events'


class NewsListView(ListView):
    model = News
    template_name = 'content/news_list.html'
    context_object_name = 'news_articles'
    ordering = ['-published_date']


class NewsDetailView(DetailView):
    model = News
    template_name = 'content/news_detail.html'
    context_object_name = 'article'


class FAQView(ListView):
    model = FAQ
    template_name = 'content/faq.html'
    context_object_name = 'faq_items'


class ContactsView(ListView):
    model = ContactPerson
    template_name = 'content/contacts.html'
    context_object_name = 'team_members'


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'content/vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(is_active=True)


class PrivacyView(TemplateView):
    template_name = 'content/privacy.html'