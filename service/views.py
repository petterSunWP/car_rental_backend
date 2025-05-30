from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import JsonResponse
from service.models import Booking, Car
from datetime import datetime
import json
from decimal import Decimal
from datetime import timedelta

def index(request):
    car_list = Car.objects.order_by("-created_at")

    context = {"car_list": car_list}
    return render(request, "service/index.html", context)

# views/booking_views.py




@csrf_exempt
def create_booking(request, car_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    # ✅ 登录检查
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "error": "Please login to book"}, status=401)

    try:
        data = json.loads(request.body)
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
    except Exception as e:
        return JsonResponse({"success": False, "error": "Invalid date format"}, status=400)

    if end_date < start_date:
        return JsonResponse({"success": False, "error": "End date must be after start date"}, status=400)

    # ✅ 查询车辆
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return JsonResponse({"success": False, "error": "Car not found"}, status=404)

    # ✅ 计算价格
    days = (end_date - start_date).days + 1
    total_price = Decimal(days) * car.daily_rental_price

    # ✅ 创建订单
    Booking.objects.create(
        car_id=car.id,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        total_cost=total_price,
        status="Pending"
    )

    return JsonResponse({"success": True, "total": float(total_price)})

def get_booked_dates(request, car_id):
    bookings = Booking.objects.filter(car_id=car_id, status__in=["Pending", "Approved"])

    booked_dates = set()
    for booking in bookings:
        day = booking.start_date
        while day <= booking.end_date:
            booked_dates.add(day.isoformat())
            day += timedelta(days=1)

    return JsonResponse({"booked_dates": sorted(booked_dates)})