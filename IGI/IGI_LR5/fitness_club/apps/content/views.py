from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.apps_utils import get_random_exercise_quote

from .forms import TermForm
from .models import (
    CompanyHistory,
    ContactPerson,
    FAQ,
    News,
    Term,
    Vacancy,
)


class HomeView(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_news'] = (
            News.objects.order_by('-published_date').first()
        )

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


# =========================================
# ТЕРМИНЫ
# =========================================

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_staff
            or self.request.user.is_superuser
        )


class TermListView(ListView):
    model = Term
    template_name = 'content/terms/term_list.html'
    context_object_name = 'terms'

    def get_queryset(self):
        queryset = Term.objects.all()

        search = self.request.GET.get('q')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort', 'term')

        if search:
            queryset = queryset.filter(
                Q(term__icontains=search)
                | Q(definition__icontains=search)
            )

        if category:
            queryset = queryset.filter(category=category)

        queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['sort'] = self.request.GET.get('sort', 'term')

        context['categories'] = [
            value
            for value, _label
            in Term.CATEGORY_CHOICES
        ]

        return context


class TermDetailView(DetailView):
    model = Term
    template_name = 'content/terms/term_detail.html'
    context_object_name = 'term'


class TermCreateView(StaffRequiredMixin, CreateView):
    model = Term
    form_class = TermForm
    template_name = 'content/terms/term_form.html'
    success_url = reverse_lazy('content:term_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить термин'
        return context


class TermUpdateView(StaffRequiredMixin, UpdateView):
    model = Term
    form_class = TermForm
    template_name = 'content/terms/term_form.html'
    success_url = reverse_lazy('content:term_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать термин'
        return context


class TermDeleteView(StaffRequiredMixin, DeleteView):
    model = Term
    template_name = 'content/terms/term_confirm_delete.html'
    success_url = reverse_lazy('content:term_list')