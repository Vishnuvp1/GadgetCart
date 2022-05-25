from django.urls import path
from . import views


urlpatterns = [path("banners/", views.banners, name="banners")]
