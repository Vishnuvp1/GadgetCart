from django.contrib.auth.models import UserManager
from django.shortcuts import render

from accounts.models import Account
from .forms import RegistrationForm
from .models import Account

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
    else:
        form = RegistrationForm()

    context = {
        'form' : form
    }
    return render(request, 'user/register.html', context)

def signin(request):
    return render(request, 'user/signin.html')


def signout(request):
    return 
    

def adminsignin(request):
    return render(request, 'adminpanel/adminsignin.html')

