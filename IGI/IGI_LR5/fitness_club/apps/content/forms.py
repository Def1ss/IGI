from django import forms

from apps.content.models import Term


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['term', 'definition', 'category']
