from django import forms
from sklearn.metrics import max_error
from .models import Musica


class PostForm(forms.ModelForm):
    url = forms.CharField(label="url", max_length=255)
    class Meta:
        model = Musica
        fields = ['url']
        exclude = ['tom','vetor','nome']