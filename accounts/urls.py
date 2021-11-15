from django.urls import path  

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('otpverification/', views.otpverification, name='otpverification'),
    
    
    
] 
