"""
URL configuration for car_rental_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from . import views
# 在 views.py 中
from service import loginViews,orderViews

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", loginViews.login_api, name="login"),
    path("register/", loginViews.register_api, name="register"),
    path("checkAuth/", loginViews.check_auth, name="checkAuth"),
    path("logout/", loginViews.logout_view, name="logout"),
    path("booking/<int:car_id>/", views.create_booking, name="create_booking"),
    path("booked-dates/<int:car_id>/", views.get_booked_dates, name="get_booked_dates"),
    path("orders/", orderViews.my_orders, name="my_orders"),
    path("cancel/<int:booking_id>/", orderViews.cancel_booking, name="cancel_booking"),
    path("pay/<int:booking_id>/", orderViews.pay_booking, name="pay_booking"), 
    path("invoice/<int:invoice_id>/download/", orderViews.download_invoice, name="download_invoice")


]
