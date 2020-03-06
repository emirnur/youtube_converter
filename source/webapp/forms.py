from django import forms
from .models import Download


class DownloadForm(forms.Form):
    class Meta:
        model = Download

    link = forms.URLField(max_length=100)
    email = forms.EmailField(max_length=100)

    def clean(self):
        cleaned_data = super(DownloadForm, self).clean()
        link = cleaned_data.get('link')
        email = cleaned_data.get('email')
        if not link and not email:
            raise forms.ValidationError('You have to write something!')

