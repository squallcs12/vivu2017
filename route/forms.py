from django import forms
from django.utils.translation import ugettext as _

from route.models import Suggest


class SuggestFilterForm(forms.Form):
    province = forms.ChoiceField(required=False, label='')

    def __init__(self, *args, **kwargs):
        super(SuggestFilterForm, self).__init__(*args, **kwargs)
        self.fields['province'].choices = [('', _('Chọn tỉnh'))] + [
            (x, x) for x in Suggest.objects.values_list('province', flat=True).distinct('province')
        ]
