from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from store.forms import ProductForm, VariantsForm
from store.models import Product
from category.forms import CategoryForm
from category.models import Category
from brand.forms import BrandForm
from brand.models import Brand


@login_required(login_url='adminsignin') 
def adminpanel(request):

    return render(request, 'adminpanel/adminpanel.html')


def adminsignin(request):

    if request.user.is_authenticated:
        return redirect('adminpanel')


    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:

            if user.is_admin:
                auth.login(request, user)
                
                return redirect('adminpanel')
            else:
                messages.info(request, 'You are not admin')
                return redirect('adminsignin')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('adminsignin')
    else:
        return render(request, 'adminpanel/adminsignin.html')



@login_required(login_url = 'adminsignin')
def adminsignout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('adminsignin')


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
            product = form.save(commit=False)
            product.slug = product.product_name.lower().replace(" ", "-")
            form.save()
            messages.success(request, 'Product added successfully')
            return redirect('productadd')

    context = {
        'form' : form
    }

    return render(request, 'adminpanel/productadd.html', context)




def productdelete(request,product_id):
    dlt = Product.objects.get(id=product_id)
    dlt.delete()
    return redirect('productlist')


def productedit(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully updated')
            return redirect('productlist')

    context = {
        'form': form
    }
    return render(request, 'adminpanel/productedit.html', context)





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
            category = form.save(commit=False)
            category.slug = category.category_name.lower().replace(" ", "-")
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('categoryadd')

    context = {
        'form' : form
    }

    return render(request, 'adminpanel/categoryadd.html', context)


def categorydelete(request,category_id):
    dlt = Category.objects.get(id=category_id)
    dlt.delete()
    return redirect('categorylist')
    

def categoryedit(request, category_id):
    category = Category.objects.get(pk=category_id)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully category updated')
            return redirect('categorylist')

    context = {
        'form': form
    }
    return render(request, 'adminpanel/categoryedit.html', context)



def brandlist(request):
    brands = Brand.objects.all()

    context = {
        'brands' : brands,
    }

    return render(request, 'adminpanel/brandlist.html', context)


def brandadd(request):

    form = BrandForm()

    if request.method == 'POST':

        form = BrandForm(request.POST, request.FILES)

        if form.is_valid():
            brand = form.save(commit=False)
            brand.slug = brand.brand_name.lower().replace(" ", "-")
            form.save()
            messages.success(request, 'Brand added successfully')
            return redirect('brandadd')

    context = {
        'form' : form
    }

    return render(request, 'adminpanel/brandadd.html', context)

def branddelete(request,brand_id):
    dlt = Brand.objects.get(id=brand_id)
    dlt.delete()
    return redirect('brandlist')


def brandedit(request, brand_id):
    product = Brand.objects.get(pk=brand_id)
    form = BrandForm(instance=product)

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully product updated')
            return redirect('brandlist')

    context = {
        'form': form
    }
    return render(request, 'adminpanel/brandedit.html', context)

def variantadd(request):
    form = VariantsForm()

    if request.method == 'POST':

        form = VariantsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Variant added successfully')
            return redirect('variantadd')

    context = {
        'form' : form
    } 

    return render(request, 'adminpanel/variantadd.html', context)