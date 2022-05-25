from django import http
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from orders.forms import OrderForm
from store.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from accounts.models import Address

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):

    url = request.META.get("HTTP_REFERER")
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product

    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass
        else:
            print("----else----")

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user
        ).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect("cart")

    # if the user is not authenticated
    else:

        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(
                cart_id=_cart_id(request)
            )  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations -> database
            # current variations -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect("cart")


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart")


def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id
        )
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart")


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if "product_id" in request.session:
            del request.session["product_id"]
        else:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                offerprice = cart_item.product.get_price()
                total += offerprice["price"] * cart_item.quantity
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, "user/cart.html", context)


@login_required(login_url="signin")
def checkout(request, total=0, quantity=0, cart_items=None):
    addresses = Address.objects.filter(user=request.user)
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            if "product_id" in request.session:
                product_id = request.session["product_id"]
                product = Product.objects.get(id=product_id)
            else:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if "product_id" in request.session:
            offerprice = product.get_price()
            quantity = 1
            total += offerprice["price"] * quantity

        else:

            for cart_item in cart_items:
                offerprice = cart_item.product.get_price()
                total += offerprice["price"] * cart_item.quantity
                quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    if request.session.has_key("coupon_id"):
        coupon_id = request.session["coupon_id"]
        request.session["couponid"] = coupon_id
        del request.session["coupon_id"]
        coupon_discount = request.session["coupon_discount"]
        coupon_discount_price = total * (coupon_discount) / 100
        request.session["coupon_discount_price"] = coupon_discount_price
        grand_total = grand_total - coupon_discount_price
        request.session["grand_total"] = grand_total
    else:
        coupon_discount_price = 0
        coupon_discount = 0

    addresses = Address.objects.filter(user=request.user)

    try:
        default_address = addresses.get(default=True)

    except ObjectDoesNotExist:
        default_address = 0

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "total": total,
        "tax": tax,
        "grand_total": grand_total,
        "addresses": addresses,
        "coupon_discount": coupon_discount,
        "coupon_discount_price": coupon_discount_price,
        "default_address": default_address,
    }

    return render(request, "user/checkout.html", context)


def buy_now(request, product_id):

    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        request.session["product_id"] = product.id
        return redirect("checkout")
    else:
        messages.error(request, "Please Login")
        return redirect("signin")
