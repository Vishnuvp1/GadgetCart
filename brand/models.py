from django.db import models
from django.urls import reverse

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    brand_image = models.ImageField(upload_to="photots/brands", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse("products_by_brand", args=[self.slug])

    def __str__(self):
        return self.brand_name

    def get_products_count(self):
        return self.product_set.all().count()
