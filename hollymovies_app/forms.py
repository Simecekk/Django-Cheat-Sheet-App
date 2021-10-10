from django import forms

from hollymovies_app.models import Movie


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    movies = forms.ModelMultipleChoiceField(queryset=Movie.objects.all())
    subject = forms.CharField(required=False)
    contact_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea)
