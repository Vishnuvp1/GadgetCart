from django.http.response import HttpResponse
from django.shortcuts import render
from banners.models import Banner
from store.models import Product

# Create your views here.


def homepage(request):

    products = Product.objects.all().filter(is_available=True)
    banners = Banner.objects.all()
    context = {"products": products, "banners": banners}
    return render(request, "user/home.html", context)
