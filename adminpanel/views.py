from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from accounts.models import Account
from banners.forms import BannerForm
from banners.models import Banner
from offer.forms import BrandOfferForm, CategoryOfferForm, ProductOfferForm
from orders.forms import OrderProductForm
from orders.models import STATUS1, Order, OrderProduct
from store.forms import ProductForm, VariantsForm
from store.models import Product
from category.forms import CategoryForm
from category.models import Category
from brand.forms import BrandForm
from brand.models import Brand
from offer.models import BrandOffer, CategoryOffer, ProductOffer


@login_required(login_url='adminsignin') 
def adminpanel(request):
    products = Product.objects.all().count()
    brands = Brand.objects.all().count()
    categories = Category.objects.all().count()
    users = Account.objects.all().count()

  

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

    products = Product.objects.all().filter(is_available=True).order_by('id')

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
            return redirect('productlist')

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
            return redirect('productlist')

    context = {
        'form' : form
    } 

    return render(request, 'adminpanel/variantadd.html', context)


def userdetails(request):
    users = Account.objects.all().order_by('id')

    context = {
        'users' : users
    }
    return render(request, 'adminpanel/userdetails.html',context )

def userdelete(request, account_id):
    user = Account.objects.get(id=account_id)
    user.delete()
    return redirect('userdetails')


def block_user(request, account_id):
    user = Account.objects.get(id=account_id)
    user.is_active = False
    user.save()
    return redirect('userdetails')


def unblock_user(request, account_id):
    user = Account.objects.get(id=account_id)
    user.is_active = True
    user.save()
    return redirect('userdetails')


def product_offer_add(request):
    form = ProductOfferForm()

    if request.method == 'POST':

        form = ProductOfferForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product Offer added successfully')
            return redirect('product_offer_list')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/product_offer_add.html', context)
    


def category_offer_add(request):
    form = CategoryOfferForm()

    if request.method == 'POST':

        form = CategoryOfferForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category Offer added successfully')
            return redirect('category_offer_list')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/category_offer_add.html', context)



def brand_offer_add(request):
    form = BrandOfferForm()

    if request.method == 'POST':

        form = BrandOfferForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Brand Offer added successfully')
            return redirect('brand_offer_list')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/brand_offer_add.html', context)


def product_offer_list(request):
    productoffers = ProductOffer.objects.all()

    context = {
        'productoffers' : productoffers
    }
    return render(request, 'adminpanel/product_offer_list.html', context)

def product_offer_delete(request, id):
    ProductOffer.objects.get(id=id).delete()
    return redirect('product_offer_list')

def category_offer_list(request):
    categoryoffers = CategoryOffer.objects.all()

    context = {
        'categoryoffers' : categoryoffers
    }
    return render(request, 'adminpanel/category_offer_list.html', context)

def category_offer_delete(request, id):
    CategoryOffer.objects.get(id=id).delete()
    return redirect('category_offer_list')

def brand_offer_list(request):
    brandoffers = BrandOffer.objects.all()

    context = {
        'brandoffers' : brandoffers
    }
    return render(request, 'adminpanel/brand_offer_list.html', context)

def brand_offer_delete(request, id):
    BrandOffer.objects.get(id=id).delete()
    return redirect('brand_offer_list')


def active_orders(request):
    exclude_list = ['Delivered', 'Canceled']
    active_orders = OrderProduct.objects.all().exclude(status__in=exclude_list)
    status = STATUS1
    context = {
        'active_orders' : active_orders,
        'status' : status
    }
    return render(request, 'adminpanel/active_orders.html', context)

def order_history(request):
    orders = OrderProduct.objects.filter(status__in=['Delivered','Canceled'])
    context  = {
        'orders' : orders
    }
    return render(request, 'adminpanel/order_history.html', context)

def active_orders_edit(request, order_id):
    order = OrderProduct.objects.get(id=order_id)
    form = OrderProductForm(instance=order)
    if request.method == 'POST':
        form = OrderProductForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Updated Successfully')
            return redirect('active_orders')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/active_orders_edit.html',context)


def banner_list(request):
    banners = Banner.objects.all()
    context = {
        'banners' : banners
    }
    return render(request, 'adminpanel/banner_list.html', context)

def banner_add(request):
    form = BannerForm()

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Banner Added Successfully.')
            return redirect('banner_list')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/banner_add.html', context)


def banner_delete(request, banner_id):
    Banner.objects.get(id=banner_id).delete()
    return redirect('banner_list')
