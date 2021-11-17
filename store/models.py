from django.db import models
from category.models import Category
from brand.models import Brand 
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name  = models.CharField(max_length=200, unique=True)
    slug          = models.SlugField(max_length=200, unique=True)
    description   = models.TextField(max_length=500, blank=True)
    price         = models.IntegerField()
    image1        = models.ImageField(upload_to='photos/products')
    image2        = models.ImageField(upload_to='photos/products')
    image3        = models.ImageField(upload_to='photos/products')
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    brand         = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


    def __str__(self):
        return self.product_name