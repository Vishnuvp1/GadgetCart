from django import forms
from django.contrib.auth import models
from django.db.models import fields
from .models import Order, OrderProduct


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "address_line_1",
            "address_line_2",
            "country",
            "state",
            "city",
            "order_note",
        ]


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ["user", "product", "quantity", "status"]
