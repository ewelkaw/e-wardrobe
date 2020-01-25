"""ewardrobe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from ewardrobe_app.views.main import MainView
from ewardrobe_app.views.welcome import WelcomeView
from ewardrobe_app.views.register import UserRegisterView
from ewardrobe_app.views.login import UserLoginView
from ewardrobe_app.views.logout import UserLogoutView
from ewardrobe_app.views.products import ProductsView
from ewardrobe_app.views.orders import OrdersView
from ewardrobe_app.views.product import ProductView


urlpatterns = [
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("ewardrobe_admin/", admin.site.urls),
    path("", WelcomeView.as_view(), name="welcome"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("main/", MainView.as_view(), name="main"),
    path("products/", ProductsView.as_view(), name="products"),
    re_path(
        "products\/(?:page=(?P<page_number>\d+))?$",
        ProductsView.as_view(),
        name="products",
    ),
    re_path("products\/(?P<id>\d+)?$", ProductView.as_view(), name="product"),
    path("orders/", OrdersView.as_view(), name="orders"),
]
