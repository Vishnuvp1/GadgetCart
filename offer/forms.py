from django.forms import ModelForm

from .models import BrandOffer, CategoryOffer, ProductOffer


class ProductOfferForm(ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['product', 'discount_offer']

class CategoryOfferForm(ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['category', 'discount_offer']

class BrandOfferForm(ModelForm):
    class Meta:
        model = BrandOffer
        fields = ['brand', 'discount_offer']


