from django import forms
from django.utils.translation import ugettext_lazy as _

from deals.models import Deal, Stage
from tools.forms import ModelForm


class DealSearchForm(forms.Form):
    s = forms.ChoiceField(
        choices=(('', _('All states')),) + Deal.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def filter(self, queryset):
        if not self.is_valid():
            return queryset

        data = self.cleaned_data
        if data.get('s'):
            queryset = queryset.filter(status=data.get('s'))

        return queryset


class DealForm(ModelForm):
    user_fields = default_to_current_user = ('owned_by',)

    stage = forms.ModelChoiceField(
        queryset=Stage.objects.all(),
        label=_('stage'),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Deal
        fields = (
            'title', 'description', 'stage', 'owned_by', 'estimated_value',
            'status')
        widgets = {
            'status': forms.RadioSelect,
        }
