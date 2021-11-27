from django.db import models
from django.db.models.deletion import CASCADE
from brand.models import Brand
from category.models import Category

# Create your models here.

class BrandOffer(models.Model):
    brand = models.OneToOneField(Brand, on_delete=CASCADE, null=True, blank=True)
    discount_offer = models.PositiveBigIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)

class CategoryOffer(models.Model):
    category = models.OneToOneField(Category, on_delete=CASCADE, null=True, blank=True)
    discount_offer = models.PositiveBigIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)

class ProductOffer(models.Model):
    product = models.OneToOneField('store.product', on_delete=CASCADE, null=True, blank=True)
    discount_offer = models.PositiveBigIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)