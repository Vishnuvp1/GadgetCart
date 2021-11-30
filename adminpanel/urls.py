from django.urls import path 

from . import views

urlpatterns = [
    path('', views.adminpanel, name="adminpanel"),
    path('adminsignin/', views.adminsignin, name='adminsignin'),
    path('adminsignout/', views.adminsignout, name='adminsignout'),

    path('productlist/', views.productlist, name="productlist"),
    path('productadd/', views.productadd, name="productadd"),
    path('productdelete/<int:product_id>/', views.productdelete, name='productdelete'),
    path('productedit/<int:product_id>/', views.productedit, name='productedit'),

    path('categorylist/', views.categorylist, name="categorylist"),
    path('categoryadd/', views.categoryadd, name="categoryadd"),
    path('categorydelete/<int:category_id>/', views.categorydelete, name='categorydelete'),
    path('categoryedit/<int:category_id>/', views.categoryedit, name='categoryedit'),
    
    path('brandlist/', views.brandlist , name='brandlist'),
    path('brandadd/', views.brandadd , name='brandadd'),
    path('branddelete/<int:brand_id>/', views.branddelete, name='branddelete'),
    path('brandedit/<int:brand_id>/', views.brandedit, name='brandedit'),

    path('variantadd/', views.variantadd, name='variantadd'),

    path('userdetails/', views.userdetails, name='userdetails'),
    path('userdelete/<int:account_id>/', views.userdelete, name='userdelete'),

    path('brand_offer_add/', views.brand_offer_add, name='brand_offer_add'),
    path('category_offer_add/', views.category_offer_add, name='category_offer_add'),
    path('product_offer_add/', views.product_offer_add, name='product_offer_add'),
    
    
]