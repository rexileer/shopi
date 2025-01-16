from django import forms

from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
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
        