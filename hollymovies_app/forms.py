from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField(required=False)
    description = forms.CharField(widget=forms.Textarea)
