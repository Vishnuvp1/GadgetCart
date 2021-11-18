from typing import Protocol
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from carts.models import Cart, CartItem
from store.models import Product
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required
from accounts.verification import send_otp, verify_otp_number

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login

from carts.views import _cart_id
from carts.models import Cart, CartItem

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password ,phone_number=phone_number)
           
            request.session['mobile'] = phone_number
            user.save()
            
            send_otp(phone_number)
            messages.success(request, 'Registration Successful.')
            return redirect('verifyaccount')
    else:
        form = RegistrationForm()

    context = {
        'form' : form
    }
    return render(request, 'user/register.html', context)

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    print(cart_item)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            if user.is_verified:
                auth.login(request, user)
                # messages.success(request, 'You are now logged in.')
                return redirect('homepage')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('signin')
    return render(request, 'user/signin.html')


@login_required(login_url = 'signin')
def signout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('signin')


def otpverification(request):
    return render(request, 'user/otp.html')


def verifyaccount(request):
    
    #Verifying the user account and updating is_verified filed
    
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        try:
            phone_number = request.session['mobile']
        except KeyError:
            messages.info(request, 'Session timeout')
            return redirect('signin')

        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)
        print('verified')
        if verified:
            user = Account.objects.get(phone_number=phone_number)
            user.is_verified = True
            user.save()
            auth.login(request, user)
            messages.success(request, 'Successfully account verified')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid OTP, please try again')
            return redirect('verifyaccount')

    return render(request, 'user/otp.html')


def mobile_login(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        phone_number = request.POST['phone']
        
        try:           
            Account.objects.get(phone_number=phone_number)
            request.session['phone_number'] = phone_number
            send_otp(phone_number)
            messages.success(request, 'OTP sent to this number')
            return redirect('mobile_login_otp_verify')
        except ObjectDoesNotExist:
            messages.error(request, 'Enter a registered mobile number')
            return redirect('signin')



def mobile_login_otp_verify(request):

    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        print('post')
        try:
            print('try')
            phone_number = request.session['phone_number']
            
        except:
            print('exept')
            messages.info(request, 'Session timeout')
            return redirect('signin')
        
        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = Account.objects.get(phone_number=phone_number)
            login(request, user)
            messages.info(request, 'Successfully logged in')
            return redirect('homepage')
        
        messages.error(request, 'Invalid OTP')
        return redirect('mobile_login_otp_verify')

    return render(request, 'user/otp.html')


def phone_number(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        phone_number = request.POST['phone']
        
        try:           
            Account.objects.get(phone_number=phone_number)
            request.session['phone_number'] = phone_number
            send_otp(phone_number)
            messages.success(request, 'OTP sent to this number')
            return redirect('reset_password_otp_verify')
        except ObjectDoesNotExist:
            messages.error(request, 'Enter a registered mobile number')
            return redirect('phone_number')

    return render(request, 'user/phone_number.html')


def reset_password_otp_verify(request):
    
    if request.method == 'POST':
        print('post')
        try:
            print('try')
            phone_number = request.session['phone_number']
            
        except:
            print('exept')
            messages.info(request, 'Session timeout')
            return redirect('phone_number')
        
        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = Account.objects.get(phone_number=phone_number)
            login(request, user)
            messages.info(request, 'Successfull')
            return redirect('set_new_password')
        
        messages.error(request, 'Invalid OTP')
        return redirect('reset_password_otp_verify')

    return render(request, 'user/reset_password_otp_verify.html')


def set_new_password(request):

    if 'phone_number' not in request.session:
        return redirect('signin')

    if request.method == 'POST':
        password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            phone_number = request.session['phone_number']
            print(phone_number)

            user = Account.objects.get(phone_number=phone_number)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password is successfully reset')
            return redirect('signin')

        else:
            messages.error(request, 'Password not matching')
            return redirect('set_new_password')

    return render(request, 'user/set_new_password.html')






