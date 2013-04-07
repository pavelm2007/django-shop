from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap_toolkit.widgets import *

class OrderFormSimple(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'your name...',
            }
        ),
        label=_('Name')
    )
    phone = forms.CharField(
        widget=BootstrapTextInput(
            attrs={
                'placeholder': '(0XX)-XXX-XX-XX',
            }
        ),
        label=_('Phone')
    )
    email = forms.EmailField(label=_('Email'))
    city = forms.CharField(max_length=50, label=_('City'))
    items = forms.CharField(widget=forms.HiddenInput)



