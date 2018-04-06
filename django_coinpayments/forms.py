from django import forms
from .utils import get_coins_list


class ChooseCoinToPayForm(forms.Form):
    currency = forms.ChoiceField(choices=get_coins_list(),
                                 widget=forms.RadioSelect(),
                                 label='',
                                 required=True)
