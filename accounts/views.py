from django.contrib import messages, auth
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required

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
            messages.success(request, 'Registration Successful.')
            return redirect('register')
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


# def forgotpassword(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         if Account.objects.filter(email=email).exists():
#             user = Account.objects.get(emial__exact=email)

#             # Reset password email
#             current_site = get_current_site(request)
#             mail_subject = 'Reset your password'
#             message = render_to_string('user/reset_password_email.html',{
#                 'user' : user,
#                 'domain' : current_site,
#                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token' : default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()

#             messages.success(request, 'Password reset email has been sent to your email address.')
#             return redirect('signin')




#         else:
#             messages.error(request, 'Account does not Exist!')
#             return redirect('forgotpassword')
#     return render(request, 'user/forgotpassword.html')

    
# def resetpassword_validate(request):
#     return HttpResponse('ok')


