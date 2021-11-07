from django import forms

from hollymovies_app.forms.validators import capitalized_validator
from hollymovies_app.models import Movie, Genre


class ContactForm(forms.Form):
    name = forms.ChoiceField(choices=Genre.GENRE_NAME_CHOICES)
    email = forms.EmailField()
    movies = forms.ModelMultipleChoiceField(queryset=Movie.objects.all())
    subject = forms.CharField(required=False, validators=[capitalized_validator])
    contact_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea)
