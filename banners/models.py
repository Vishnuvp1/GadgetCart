from django.db import models
from django.db.models.deletion import CASCADE

from store.models import Product
from brand.models import Brand
from category.models import Category

# Create your models here.


class Banner(models.Model):
    banner_name = models.CharField(max_length=100, unique=True)
    banner_img = models.ImageField(upload_to="photos/banners")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.banner_name
