from django import forms
from bootstrap_toolkit.widgets import *

class OrderFormSimple(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'your name...',
            }
        )
    )
    phone = forms.CharField(
        widget=BootstrapTextInput(
            attrs={
                'placeholder': '(0XX)-XXX-XX-XX',
            }
        ),
    )
    email = forms.EmailField()
    items = forms.CharField(widget=forms.HiddenInput)
    city = forms.CharField(max_length=50)
    office = forms.ComboField()



