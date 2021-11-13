from django.db import models

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(max_length = 100, unique = True)
    description = models.TextField(max_length = 255, blank = True)
    brand_image = models.ImageField(upload_to = 'photots/brands', blank = True)

    def __str__(self):
        return self.brand_name