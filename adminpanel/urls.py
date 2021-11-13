from django.urls import path 

from . import views

urlpatterns = [
    path('', views.adminpanel, name="adminpanel"),
    path('productlist', views.productlist, name="productlist"),
    path('productadd', views.productadd, name="productadd"),
    path('categorylist', views.categorylist, name="categorylist"),
    path('categoryadd', views.categoryadd, name="categoryadd"),
    
]