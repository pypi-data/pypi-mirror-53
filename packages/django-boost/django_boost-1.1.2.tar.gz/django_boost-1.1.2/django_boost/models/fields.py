from django import forms
from django.db import models
from django.db.models.fields import CharField, TextField

from django_boost.forms import fields
from django_boost.validators import validate_json


class JsonField(TextField):
    empty_strings_allowed = False
    default_validators = [validate_json]


class ColorCodeFiled(CharField):
    """Field for storing hexadecimal color code like `FFEEDD`."""

    default_validators = []

    def __init__(self, *args, upper=False, lower=False, **kwargs):
        kwargs.update({"max_length": 7})
        if upper and lower:
            raise AssertionError(
                'upper and lower can not be specified at the same time.'
                ' Please specify only one or the other.')
        self.upper = upper
        self.lower = lower
        if self.upper:
            self.normalize = self._upper_convert
        elif self.lower:
            self.normalize = self._lower_convert
        else:
            self.normalize = self._no_convert
        super().__init__(*args, **kwargs)

    def _upper_convert(self, value):
        return value.upper()

    def _lower_convert(self, value):
        return value.lower()

    def _no_convert(self, value):
        return value

    def pre_save(self, model_instance, add):
        return self.normalize(super().pre_save(model_instance, add))

    def to_python(self, value):
        return self.normalize(super().to_python(value))

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': fields.ColorCodeField,
            **kwargs,
        })


class SplitDateTimeField(models.DateTimeField):

    def formfield(self, **kwargs):
        kwargs.update({'form_class': forms.SplitDateTimeField})
        return super().formfield(**kwargs)
