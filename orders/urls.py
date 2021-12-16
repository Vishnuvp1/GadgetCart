from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('cash_on_delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('razorpay_payment_verification/', views.razorpay_payment_verification, name='razorpay_payment_verification'),
    path('payment_failed', views.payment_failed, name='payment_failed'),

    path('order_pdf', views.order_pdf, name='order_pdf'),
    
]