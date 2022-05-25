from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import Product, ReviewRating
from .models import Variation


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_name",
            "description",
            "stock",
            "price",
            "brand",
            "category",
            "image1",
            "image2",
            "image3",
        ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs["placeholder"] = "Enter Product Name"
        self.fields["description"].widget.attrs["placeholder"] = "Enter Description"
        self.fields["stock"].widget.attrs["placeholder"] = "Enter stock"
        self.fields["price"].widget.attrs["placeholder"] = "Enter price"
        self.fields["category"].widget.attrs["placeholder"] = "Select category"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control mt-1 mb-2 "


class VariantsForm(ModelForm):
    class Meta:
        model = Variation
        fields = ["product", "variation_category", "variation_value"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ["subject", "review", "rating"]
