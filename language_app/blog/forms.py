"""Custom form classes go here.
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms

from .models import Definition

class DefinitionForm(forms.ModelForm):
    class Meta:
        model = Definition
        fields = ['phrase', 'description', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'size': 5})
        }
        help_texts = {
            'categories': 'Select up to five relevant categories.'
        }