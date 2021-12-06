import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.api import success
from django.db.models.aggregates import Sum
from django.shortcuts import redirect, render
from accounts.models import Account
from banners.forms import BannerForm
from banners.models import Banner
from offer.forms import BrandOfferForm, CategoryOfferForm, CouponForm, ProductOfferForm
from orders.forms import OrderProductForm
from orders.models import STATUS1, Order, OrderProduct, Payment
from store.forms import ProductForm, VariantsForm
from store.models import Product
from category.forms import CategoryForm
from category.models import Category
from brand.forms import BrandForm
from brand.models import Brand
from offer.models import BrandOffer, CategoryOffer, Coupon, ProductOffer, RedeemedCoupon
from django.utils import timezone
from datetime import date, timedelta


@login_required(login_url='adminsignin') 
def adminpanel(request):
    products = Product.objects.all().count()
    brands = Brand.objects.all()
    categories = Category.objects.all().count()
    users = Account.objects.all().count()
    current_year = timezone.now().year

    total_orders = Order.objects.filter(is_ordered=True).count()
    total_revenue = Order.objects.aggregate(Sum('order_total'))
    total_profit = float(total_revenue['order_total__sum'])


    

    paypal_count = Payment.objects.filter(payment_method="PayPal").count()
    razorpay_count = Payment.objects.filter(payment_method='razorpay').count()

    new_count = OrderProduct.objects.filter(status='New').count()
    placed_count = OrderProduct.objects.filter(status='Placed').count()
    shipped_count = OrderProduct.objects.filter(status='Shipped').count()
    accepted_count = OrderProduct.objects.filter(status='Accepted').count()
    delivered_count = OrderProduct.objects.filter(status='Delivered').count()
    cancelled_count = OrderProduct.objects.filter(status='Canceled').count()


    # daily orders
    today = date.today()
    today_1 = today - timedelta(days=1)
    today_2 = today - timedelta(days=2)
    today_3 = today - timedelta(days=3)
    today_4 = today - timedelta(days=4)
    today_5 = today - timedelta(days=5)
    today_6 = today - timedelta(days=6)
    today_7 = today - timedelta(days=7)

    last_week_days=[
        today_6.strftime("%a %m/%d/%Y"),
        today_5.strftime("%a %m/%d/%Y"),
        today_4.strftime("%a %m/%d/%Y"),
        today_3.strftime("%a %m/%d/%Y"),
        today_2.strftime("%a %m/%d/%Y"),
        today_1.strftime("%a %m/%d/%Y"),
        today.strftime("%a %m/%d/%Y"),
    ]

    today_order = OrderProduct.objects.filter(created_at__range=[today_1, today]).count()
    today_1_order = OrderProduct.objects.filter(created_at__range=[today_2, today_1]).count()
    today_2_order = OrderProduct.objects.filter(created_at__range=[today_3, today_2]).count()
    today_3_order = OrderProduct.objects.filter(created_at__range=[today_4, today_3]).count()
    today_4_order = OrderProduct.objects.filter(created_at__range=[today_5, today_4]).count()
    today_5_order = OrderProduct.objects.filter(created_at__range=[today_6, today_5]).count()
    today_6_order = OrderProduct.objects.filter(created_at__range=[today_7, today_6]).count()

    last_week_orders = [today_6_order,today_5_order,today_4_order,today_3_order,today_2_order,today_1_order,today_order]

    # orders chart data
    labels1 = []
    data1 = []

    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')[:10]
    for order in orders:
        labels1.append(order.updated_at.day)
        data1.append(order.order_total)

    brands_list = list()
    products_count = list()
    for i in brands:
        brands_list.append(i.brand_name)
        products_count.append(Product.objects.filter(brand__brand_name=i.brand_name).count())

   

    context = {
        'brands': brands,
        'products': products,
        'categories' : categories,
        'users' : users,
        'total_orders': total_orders,
        'total_revenue': total_revenue['order_total__sum'],
        'total_profit' : total_profit,

        
        'month_name': ['January', 'February', 'March', 'May', 'June', 'July', 'August', 'September', 'October',
                       'November', 'December'],

        'payment_method_status': [ paypal_count, razorpay_count],

        'status_counter':[new_count, placed_count, shipped_count, accepted_count, delivered_count, cancelled_count],

        # Weekly orders
        'last_week_days' : last_week_days,
        'last_week_orders' : last_week_orders,

        'labels': labels1,
        'data': data1,

        'brands_list': brands_list,
        'products_count': products_count,

    }

    return render(request, 'adminpanel/adminpanel.html', context)


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
    active_orders = OrderProduct.objects.all().exclude(status__in=exclude_list).order_by('-id')
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


def report(request):
    brands = Brand.objects.all().order_by('-id')
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-id')
    orders = OrderProduct.objects.all()

    if request.GET.get('from'):
        date_from = datetime.datetime.strptime(request.GET.get('from'), "%Y-%m-%d")
        date_to = datetime.datetime.strptime(request.GET.get('to'), "%Y-%m-%d")
        date_to += datetime.timedelta(days=1)
        orders = orders.filter(created_at__range=[date_from, date_to])
        print(orders)

    context = {
        'categories' : categories,
        'brands': brands,
        'products': products,
        'orders': orders,
    }
    return render(request, 'adminpanel/report.html', context)


def coupon_list(request):
    coupons = Coupon.objects.all()

    context = {
        'coupons' : coupons
    }
    return render(request, 'adminpanel/coupon_list.html', context)

def coupon_add(request):
    form = CouponForm

    if request.method == 'POST':
        form = CouponForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon Added Successfully.')
            return redirect('coupon_list')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/coupon_add.html', context)

def coupon_delete(request, coupon_id):
    Coupon.objects.get(id=coupon_id).delete()
    return redirect('coupon_list')


def redeemed_coupons(request):
    redeemed_coupons = RedeemedCoupon.objects.all()
    
    context = {
        'redeemed_coupons' : redeemed_coupons
    }
    return render(request, 'adminpanel/redeemed_coupons.html', context)