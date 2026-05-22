from django.template.context import BaseContext


def patch_template_context_copy():
    """Keep Django admin inclusion tags working on Python 3.14.

    Django 6.0.4 still uses copy(super()) inside BaseContext.__copy__.
    On Python 3.14 that no longer returns a mutable context-like object, which
    breaks changelist and change-form rendering in the admin.
    """

    def fixed_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = fixed_copy
