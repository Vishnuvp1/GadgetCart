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
    path('block_user/<int:account_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:account_id>/', views.unblock_user, name='unblock_user'),


    path('brand_offer_add/', views.brand_offer_add, name='brand_offer_add'),
    path('category_offer_add/', views.category_offer_add, name='category_offer_add'),
    path('product_offer_add/', views.product_offer_add, name='product_offer_add'),

    path('product_offer_list/', views.product_offer_list, name='product_offer_list'),
    path('product_offer_delete/<int:id>', views.product_offer_delete, name='product_offer_delete'),
    path('category_offer_list/', views.category_offer_list, name='category_offer_list'),
    path('category_offer_delete/<int:id>', views.category_offer_delete, name='category_offer_delete'),
    path('brand_offer_list/', views.brand_offer_list, name='brand_offer_list'),
    path('brand_offer_delete/<int:id>', views.brand_offer_delete, name='brand_offer_delete'),

    path('active_orders/', views.active_orders, name='active_orders'),
    path('active_orders_edit/<int:order_id>/', views.active_orders_edit, name='active_orders_edit'),
    path('order_history/', views.order_history, name='order_history'),

    path('banner_list/', views.banner_list, name='banner_list'),
    path('banner_add/', views.banner_add, name='banner_add'),
    path('banner_delete/<int:banner_id>', views.banner_delete, name='banner_delete'),

    path('report/', views.report, name='report'),

    path('coupon_list/', views.coupon_list, name='coupon_list'),
    path('coupon_add/', views.coupon_add, name='coupon_add'),
    path('coupon_delete/<int:coupon_id>/', views.coupon_delete, name='coupon_delete'),
    path('redeemed_coupons/', views.redeemed_coupons, name='redeemed_coupons'),

    path('brands_pdf/', views.brands_pdf, name='brands_pdf')
  
    
]