from django.urls import path 

from . import views

urlpatterns = [
    path('', views.adminpanel, name="adminpanel"),
    path('productlist/', views.productlist, name="productlist"),
    path('productadd/', views.productadd, name="productadd"),
    path('categorylist/', views.categorylist, name="categorylist"),
    path('categoryadd/', views.categoryadd, name="categoryadd"),
    path('adminsignin/', views.adminsignin, name='adminsignin'),
    path('adminsignout/', views.adminsignout, name='adminsignout'),
    path('productdelete/<int:product_id>/', views.productdelete, name='productdelete'),
    path('brandlist', views.brandlist , name='brandlist'),
    path('brandadd', views.brandadd , name='brandadd'),
    
    
]