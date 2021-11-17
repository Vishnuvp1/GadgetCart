from django.urls import path  

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('verifyaccount/', views.verifyaccount, name='verifyaccount'),
    path('mobile_login/', views.mobile_login, name='mobile_login'),
    path('mobile_login_otp_verify/', views.mobile_login_otp_verify, name='mobile_login_otp_verify')
    
] 
