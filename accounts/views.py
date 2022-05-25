from functools import reduce
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, CartItem
from store.models import Product
from .forms import AddressForm, RegistrationForm, UserForm, UserProfileForm
from .models import Account, Address, UserProfile
from django.contrib.auth.decorators import login_required
from accounts.verification import send_otp, verify_otp_number

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

from orders.models import Order, OrderProduct

# Create your views here.


def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                phone_number=phone_number,
            )

            request.session["mobile"] = phone_number
            # user.save()

            # Create User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = "default/default-user.png"
            profile.save()

            # Send otp
            send_otp(phone_number)
            messages.info(request, "Enter Your Phone Number.")
            return redirect("verifyaccount")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "user/register.html", context)


def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = Account.objects.get(email=email)
            print(user)
            if not user.is_active:
                messages.info(request, "Acces Denied")
                return redirect("signin")
        except:
            pass

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart item from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)

                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            # Changed to is_verified to is_active
            if user.is_active:
                auth.login(request, user)
                messages.success(request, "You are now logged in.")
                url = request.META.get("HTTP_REFERER")
                try:
                    query = requests.utils.urlparse(url).query
                    # next=/cart/checkout/
                    params = dict(x.split("=") for x in query.split("&"))
                    if "next" in params:
                        nextPage = params["next"]
                        return redirect(nextPage)

                except:
                    return redirect("homepage")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("signin")
    return render(request, "user/signin.html")


@login_required(login_url="signin")
def signout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect("signin")


def otpverification(request):
    return render(request, "user/otp.html")


def verifyaccount(request):

    # Verifying the user account and updating is_verified filed

    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        try:
            phone_number = request.session["mobile"]
        except KeyError:
            messages.info(request, "Session timeout")
            return redirect("signin")

        otp = request.POST.get("otp")
        verified = verify_otp_number(phone_number, otp)
        print("verified")
        if verified:
            user = Account.objects.get(phone_number=phone_number)
            user.is_verified = True
            user.save()
            auth.login(request, user)
            messages.success(request, "Successfully account verified")
            return redirect("homepage")
        else:
            messages.error(request, "Invalid OTP, please try again")
            return redirect("verifyaccount")

    return render(request, "user/otp.html")


def resent_otp(request):
    phone_number = request.session["mobile"]
    send_otp(phone_number)
    return redirect("verifyaccount")


def mobile_login(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        phone_number = request.POST["phone"]

        try:
            Account.objects.get(phone_number=phone_number)
            request.session["phone_number"] = phone_number
            send_otp(phone_number)
            messages.success(request, "OTP sent to this number")
            return redirect("mobile_login_otp_verify")
        except ObjectDoesNotExist:
            messages.error(request, "Enter a registered mobile number")
            return redirect("signin")


def mobile_login_otp_verify(request):

    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        print("post")
        try:
            print("try")
            phone_number = request.session["phone_number"]

        except:
            print("exept")
            messages.info(request, "Session timeout")
            return redirect("signin")

        otp = request.POST.get("otp")
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = Account.objects.get(phone_number=phone_number)
            login(request, user)
            messages.info(request, "Successfully logged in")
            return redirect("homepage")

        messages.error(request, "Invalid OTP")
        return redirect("mobile_login_otp_verify")

    return render(request, "user/otp.html")


def phone_number(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        phone_number = request.POST["phone"]

        try:
            Account.objects.get(phone_number=phone_number)
            request.session["phone_number"] = phone_number
            send_otp(phone_number)
            messages.success(request, "OTP sent to this number")
            return redirect("reset_password_otp_verify")
        except ObjectDoesNotExist:
            messages.error(request, "Enter a registered mobile number")
            return redirect("phone_number")

    return render(request, "user/phone_number.html")


def reset_password_otp_verify(request):

    if request.method == "POST":
        print("post")
        try:
            print("try")
            phone_number = request.session["phone_number"]

        except:
            print("exept")
            messages.info(request, "Session timeout")
            return redirect("phone_number")

        otp = request.POST.get("otp")
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = Account.objects.get(phone_number=phone_number)
            login(request, user)
            messages.info(request, "Successfull")
            return redirect("set_new_password")

        messages.error(request, "Invalid OTP")
        return redirect("reset_password_otp_verify")

    return render(request, "user/reset_password_otp_verify.html")


def set_new_password(request):

    if "phone_number" not in request.session:
        return redirect("signin")

    if request.method == "POST":
        password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            phone_number = request.session["phone_number"]
            print(phone_number)

            user = Account.objects.get(phone_number=phone_number)
            user.set_password(password)
            user.save()
            messages.success(request, "Password is successfully reset")
            return redirect("signin")

        else:
            messages.error(request, "Password not matching")
            return redirect("set_new_password")

    return render(request, "user/set_new_password.html")


@login_required(login_url="signin")
def dashboard(request):
    orders = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id, is_ordered=True
    )
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {"orders_count": orders_count, "userprofile": userprofile}
    return render(request, "user/dashboard.html", context)


@login_required(login_url="signin")
def my_orders(request):
    orders = OrderProduct.objects.filter(user=request.user).order_by("-created_at")
    context = {"orders": orders}
    return render(request, "user/my_orders.html", context)


@login_required(login_url="signin")
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated.")
            return redirect("edit_profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "userprofile": userprofile,
    }
    return render(request, "user/edit_profile.html", context)


@login_required(login_url="signin")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password Updated Successfully.")
                return redirect("change_password")
            else:
                messages.error(request, "Please Enter Valid Current Password.")
                return redirect("change_password")
        else:
            messages.error(request, "Password Does not Match!")
            return redirect("change_password")

    return render(request, "user/change_password.html")


@login_required(login_url="signin")
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    tax = 0
    g_total = 0
    for i in order_detail:
        offerprice = i.product.get_price()
        subtotal += offerprice["price"] * i.quantity
    tax = (2 * subtotal) / 100
    g_total = subtotal + tax
    context = {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal,
        "tax": tax,
        "g_total": g_total,
    }
    return render(request, "user/order_detail.html", context)


@login_required(login_url="signin")
def my_address(request):
    form = AddressForm()
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST)
        print(request.POST)
        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Successfuly added new address")
            return redirect("my_address")

    context = {"form": form, "addresses": addresses}

    return render(request, "user/my_address.html", context)


@login_required(login_url="signin")
def edit_address(request, pk):
    address = Address.objects.get(pk=pk)
    form = AddressForm(instance=address)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)

        if form.is_valid:
            form.save()
            messages.success(request, "Your Address is updated")
            return redirect("my_address")

    context = {"form": form}
    return render(request, "user/edit_address.html", context)


@login_required(login_url="signin")
def delete_address(request, pk):
    Address.objects.get(id=pk).delete()
    return redirect("my_address")


@login_required(login_url="signin")
def default_address(request, pk):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    address = Address.objects.get(pk=pk)
    address.default = True
    address.save()
    messages.success(request, "Default Address Changed")
    return redirect("my_address")


@login_required(login_url="signin")
def cancel_order(request, pk):
    product = OrderProduct.objects.get(pk=pk)
    print(product)
    product.status = "Canceled"
    product.save()
    item = Product.objects.get(pk=product.product.id)
    item.stock += product.quantity
    item.save()
    return redirect("my_orders")
