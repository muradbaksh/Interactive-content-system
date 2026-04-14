from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title.strip()