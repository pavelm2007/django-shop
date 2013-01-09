from django import forms
from bootstrap_toolkit.widgets import *

class OrderFormSimple(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name',
            }
        )
    )
    city = forms.CharField(max_length=50)
    phone = forms.CharField(widget=BootstrapTextInput())
    email = forms.EmailField()
    items = forms.CharField(widget=forms.HiddenInput)



