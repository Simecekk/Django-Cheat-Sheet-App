from django.core.exceptions import ValidationError
from django import forms

"""
Django docs:

If the built-in Field classes don't meet your needs, you can easily create custom Field classes.
To do this, just create a subclass of django.forms.Field.
Its only requirements are that it implement a clean() method and that its __init__() 
method accept the core arguments mentioned above (required, label, initial, widget, help_text).

NOTE: In this example we just wanted to change validation method on the CharField so we are subclassing the CharField
instead of the basic forms.Field
"""


class CapitalizedCharField(forms.CharField):
    def validate(self, value):
        super(CapitalizedCharField, self).validate(value)
        if value[0].islower():
            raise ValidationError('Value must be capitalized.')

    def clean(self, value):
        return value.capitalized()
