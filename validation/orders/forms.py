# Python.DjangoInputValidation.json -> "Django Input Validation Python" [InputValidation]
# Supporting file: the form validated in orders/views.py (no is_valid call here)
from django import forms


class ShippingAddressForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    line1 = forms.CharField(max_length=200)
    city = forms.CharField(max_length=80)
    postal_code = forms.RegexField(regex=r"^[A-Za-z0-9 -]{3,10}$")
    country = forms.ChoiceField(choices=[("US", "United States"), ("IL", "Israel"), ("DE", "Germany")])
