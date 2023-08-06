from django.core.exceptions import (ImproperlyConfigured,
                                    MultipleObjectsReturned,
                                    ObjectDoesNotExist)


class FormUserKwargsMixin:
    """Mixin to add `User model` to form instance variable."""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


class MuchedObjectGetMixin:
    """
    Object of the condition that matches the form input content.

    Or mixin to add a method to get the query set.
    """

    model = None
    queryset = None
    raise_exception = False

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            elif self._meta.model:
                return self._meta.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        self.model_class = self.queryset.model
        return self.queryset.all()

    def get_list(self, queryset=None):
        """Return matched object queryset."""
        if queryset is None:
            query = self.get_queryset()
        else:
            query = queryset
        return query.filter(**self.cleaned_data)

    def get_object(self, queryset=None):
        """Return matched object."""
        try:
            return self.get_list(queryset).get()
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            if self.raise_exception:
                raise e
            return None
