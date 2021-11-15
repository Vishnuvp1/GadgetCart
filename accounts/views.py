from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required
from accounts.verification import send_otp, verify_otp_number

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
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            request.session['mobile'] = phone_number
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
        return redirect('home')

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



