from django import forms

from .models import ShippingAdress


class ShippingAdressForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        fields = [
            "full_name",
            "email",
            "country",
            "city",
            "street",
            "apartment",
            "zip",
        ]
        exclude = ["user"]
        