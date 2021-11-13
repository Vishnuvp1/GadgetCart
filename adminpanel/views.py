from django.shortcuts import redirect, render
from store.forms import ProductForm
from store.models import Product
from category.forms import CategoryForm
from category.models import Category



def adminpanel(request):

    return render(request, 'adminpanel/adminpanel.html')

def productlist(request):

    products = Product.objects.all().filter(is_available=True)


    context = {
        'products' : products,
    }


    return render(request, 'adminpanel/productlist.html',context)


def productadd(request):

    form = ProductForm()

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('productlist')

    context = {
        'form' : form
    }

    return render(request, 'adminpanel/productadd.html', context)



def categorylist(request):

    categories = Category.objects.all()

    context = {
        'categories' : categories,
    }

    return render(request, 'adminpanel/categorylist.html', context)


def categoryadd(request):

    form = CategoryForm()

    if request.method == 'POST':

        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('categorylist')

    context = {
        'form' : form
    }

    return render(request, 'adminpanel/categoryadd.html', context)

    