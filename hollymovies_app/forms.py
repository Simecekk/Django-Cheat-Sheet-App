from django import forms
from django.core.exceptions import ValidationError

from hollymovies_app.models import Movie


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class CapitalizedCharField(forms.CharField):

    def validate(self, value):
        if value[0].islower():
            raise ValidationError('Value must be capitalized.')

    def clean(self, value):
        return value.capitalized()


class ContactForm(forms.Form):
    name = CapitalizedCharField()
    email = forms.EmailField()
    movies = forms.ModelMultipleChoiceField(queryset=Movie.objects.all())
    subject = forms.CharField(required=False, validators=[capitalized_validator])
    contact_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'genres']
