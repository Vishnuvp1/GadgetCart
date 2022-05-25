from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import UUIDField
from brand.models import Brand
from category.models import Category
from accounts.models import Account

# Create your models here.


class BrandOffer(models.Model):
    brand = models.OneToOneField(Brand, on_delete=CASCADE, null=True, blank=True)
    discount_offer = models.PositiveBigIntegerField(help_text="Offer in percentage")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class CategoryOffer(models.Model):
    category = models.OneToOneField(Category, on_delete=CASCADE, null=True, blank=True)
    discount_offer = models.PositiveBigIntegerField(help_text="Offer in percentage")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class ProductOffer(models.Model):
    product = models.OneToOneField(
        "store.product", on_delete=CASCADE, null=True, blank=True
    )
    discount_offer = models.PositiveBigIntegerField(help_text="Offer in percentage")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text="Offer in percentage", null=True)
    limit = models.PositiveIntegerField(null=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_name


class RedeemedCoupon(models.Model):
    user = models.ForeignKey(Account(), on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.coupon.coupon_name}"
