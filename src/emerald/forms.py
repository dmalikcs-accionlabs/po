from utils.forms import BaseOnlyFormClassAdd

from django import forms

class UploadForm(BaseOnlyFormClassAdd):
    email = forms.EmailField()
    subject = forms.CharField(max_length=20)
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    file = forms.FileField()
