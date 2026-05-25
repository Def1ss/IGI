from django import forms

from apps.content.models import Term


class TermForm(forms.ModelForm):
    class Meta:
        model = Term

        fields = [
            'term',
            'definition',
            'category',
        ]

        widgets = {
            'term': forms.TextInput(attrs={
                'placeholder': 'Введите термин'
            }),

            'definition': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Введите описание термина'
            }),

            'category': forms.Select(),
        }