from django.db import models
from django.db.models.deletion import CASCADE
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


    def get_price(self):
        try:
            if self.productoffer.is_active:
                print('--------product----------')
                offer_price = (self.price / 100) * self.productoffer.discount_offer
                price = self.price - offer_price
                return {'price': price, 'discount': self.productoffer.discount_offer}
            raise
        except:
            try:
                if self.category.categoryoffer.is_active:
                    print('------category--------')
                    offer_price = (self.price / 100) * self.category.categoryoffer.discount_offer
                    price = self.price - offer_price
                    return {'price': price, 'discount': self.category.categoryoffer.discount_offer}
                raise
            except:
                try:
                    if self.brand.brandoffer.is_active:
                        print('------brand-------')
                        offer_price = (self.price / 100) * self.brand.brandoffer.discount_offer
                        price = self.price - offer_price
                        return {'price': price, 'discount': self.brand.brandoffer.discount_offer}
                    raise
                except:
                    print('----else----')
                return {'price': self.price}


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color' , is_active=True)

    

variation_category_choices = (
    ('color', 'Color'),
    
)

class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


