from collections import defaultdict

from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'cols': 40, 'rows': 4}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ModelForm(forms.ModelForm):
    user_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.user_fields:
            self._only_active_and_initial_users(
                self.fields[field],
                self.instance and getattr(
                    self.instance,
                    '%s_id' % field,
                    None)
            )

    def _only_active_and_initial_users(self, formfield, pk):
        d = defaultdict(list)
        for user in User.objects.filter(Q(is_active=True) | Q(pk=pk)):
            d[user.is_active].append((
                formfield.prepare_value(user),
                formfield.label_from_instance(user),
            ))
        choices = [(_('Active'), d.get(True, []))]
        if d.get(False):
            choices[0:0] = d.get(False)
        formfield.choices = choices
