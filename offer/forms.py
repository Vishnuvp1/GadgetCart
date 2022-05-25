from django import forms
from django.forms import ModelForm, widgets

from .models import BrandOffer, CategoryOffer, Coupon, ProductOffer


class ProductOfferForm(ModelForm):
    class Meta:
        model = ProductOffer
        fields = ["product", "discount_offer"]


class CategoryOfferForm(ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ["category", "discount_offer"]


class BrandOfferForm(ModelForm):
    class Meta:
        model = BrandOffer
        fields = ["brand", "discount_offer"]


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ["coupon_name", "coupon_code", "discount", "valid_from", "valid_to"]

        widgets = {
            "valid_from": forms.DateInput(attrs={"type": "date"}),
            "valid_to": forms.DateInput(attrs={"type": "date"}),
        }
