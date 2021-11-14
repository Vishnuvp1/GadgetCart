from django.urls import path  

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    # path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    # path('resetpassword_validate/<uid64>/<token>', views.resetpassword_validate, name='resetpassword_validate')
    
    
] 
