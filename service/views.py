from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Car


def index(request):
    car_list = Car.objects.order_by("-created_at")

    context = {"car_list": car_list}
    return render(request, "service/index.html", context)
