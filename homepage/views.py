from django.http.response import HttpResponse
from django.shortcuts import render
from store.models import Product

# Create your views here.

def homepage(request):
    
    products = Product.objects.all().filter(is_available=True)


    context = {
        'products' : products,
    }

    return render(request,'user/home.html',context)