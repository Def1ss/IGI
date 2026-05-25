from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220, blank=True)
    summary = models.CharField(
        max_length=250,
        help_text="Одно предложение, обобщающее новость."
    )
    full_text = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    published_date = models.DateTimeField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_news'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    position = models.CharField(max_length=150)
    description = models.TextField()
    salary = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.position


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question


class ContactPerson(models.Model):
    full_name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='staff/', null=True, blank=True)

    role = models.CharField(
        max_length=150,
        help_text="Описание работы сотрудника"
    )

    phone = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.full_name


class CompanyHistory(models.Model):
    year = models.IntegerField(unique=True)
    event = models.TextField()

    class Meta:
        ordering = ['year']

    def __str__(self):
        return f"{self.year}: {self.event[:30]}..."


# =========================================
# ТЕРМИНЫ
# =========================================

class Term(models.Model):
    CATEGORY_CHOICES = [
        ('fitness', 'Фитнес'),
        ('nutrition', 'Питание'),
        ('workout', 'Тренировки'),
        ('health', 'Здоровье'),
        ('other', 'Другое'),
    ]

    term = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Термин'
    )

    definition = models.TextField(
        verbose_name='Определение'
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория'
    )

    added_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_date = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['term']
        verbose_name = 'Термин'
        verbose_name_plural = 'Термины'

    def __str__(self):
        return self.term