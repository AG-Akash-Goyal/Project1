from django import forms
from .models import FAQ


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = [ 'question']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()
    areaid=forms.IntegerField()


class CatForm(forms.Form):
    catid = forms.IntegerField()
    areaid=forms.IntegerField()