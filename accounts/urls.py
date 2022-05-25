from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("verifyaccount/", views.verifyaccount, name="verifyaccount"),
    path("resent_otp/", views.resent_otp, name="resent_otp"),
    path("mobile_login/", views.mobile_login, name="mobile_login"),
    path(
        "mobile_login_otp_verify/",
        views.mobile_login_otp_verify,
        name="mobile_login_otp_verify",
    ),
    path("phone_number/", views.phone_number, name="phone_number"),
    path(
        "reset_password_otp_verify/",
        views.reset_password_otp_verify,
        name="reset_password_otp_verify",
    ),
    path("set_new_password/", views.set_new_password, name="set_new_password"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.dashboard, name="dashboard"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("order_detail/<int:order_id>/", views.order_detail, name="order_detail"),
    path("my_address/", views.my_address, name="my_address"),
    path("edit_address/<int:pk>/", views.edit_address, name="edit_address"),
    path("delete_address/<int:pk>/", views.delete_address, name="delete_address"),
    path("default_address/<int:pk>/", views.default_address, name="default_address"),
    path("cancel_order/<int:pk>/", views.cancel_order, name="cancel_order"),
]
