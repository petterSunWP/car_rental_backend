# views/order_views.py

from django.shortcuts import render, redirect
from service.models import Booking, Car, Payment, Invoice
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

def my_orders(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("/")

    bookings = Booking.objects.filter(user_id=user_id).order_by("-created_at")

    # 为每个 booking 附上对应车辆
    for booking in bookings:
        booking.car = None
        booking.payment = None
        booking.invoice = None
        booking.is_past = booking.end_date < date.today()

        try:
            booking.car = Car.objects.get(id=booking.car_id)
        except Car.DoesNotExist:
            pass

        try:
            booking.payment = Payment.objects.get(booking_id=booking.id, status="Paid")
        except Payment.DoesNotExist:
            pass

        try:
            booking.invoice = Invoice.objects.get(booking=booking)
        except Invoice.DoesNotExist:
            pass

    return render(request, "service/orders.html", {"bookings": bookings})



@csrf_exempt
def cancel_booking(request, booking_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    try:
        booking = Booking.objects.get(id=booking_id, user_id=user_id)
    except Booking.DoesNotExist:
        return JsonResponse({"success": False, "error": "Booking not found"}, status=404)

    if booking.status in ["Rejected"]:
        return JsonResponse({"success": False, "error": "Already cancelled"}, status=400)

    if booking.end_date < date.today():
        return JsonResponse({"success": False, "error": "Cannot cancel past bookings"}, status=400)

    # ✅ 设置状态为 Rejected
    booking.status = "Cancelled"
    booking.save()
    try:
            payment = Payment.objects.get(booking_id=booking.id, status="Paid")
            payment.status = "Refunded"
            payment.save()
    except Payment.DoesNotExist:
            pass  # 未付款就不用管
     # ✅ 如果已开票，则标记发票为 Voided
    try:
        invoice = Invoice.objects.get(booking=booking)
        invoice.status = "Voided"
        invoice.save()
    except Invoice.DoesNotExist:
        pass  # 没开票就不用改

    return JsonResponse({"success": True, "message": "Booking cancelled successfully"})



@csrf_exempt
def pay_booking(request, booking_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "error": "Please login"}, status=401)

    try:
        booking = Booking.objects.get(id=booking_id, user_id=user_id)
    except Booking.DoesNotExist:
        return JsonResponse({"success": False, "error": "Booking not found"}, status=404)

    if booking.status != "Approved":
        return JsonResponse({"success": False, "error": "Only approved bookings can be paid"}, status=400)

    # ✅ 检查是否已支付
    if Payment.objects.filter(booking_id=booking.id, status="Paid").exists():
        return JsonResponse({"success": False, "error": "Already paid"}, status=400)

    # ✅ 创建付款记录
    Payment.objects.create(
        booking_id=booking.id,
        amount=booking.total_cost,
        payment_method="CreditCard",  # 假设目前固定，后期可扩展
        status="Paid"
    )
    if not hasattr(booking, "invoice"):
        Invoice.objects.create(
            booking=booking,
            amount=booking.total_cost,
            status="Issued"  # 默认开票但未标记为“已支付”
        )

    return JsonResponse({"success": True, "message": "Payment successful!"})

# views/invoice_views.py


def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    booking = invoice.booking
    car = get_object_or_404(Car, id=booking.car_id)

    context = {
        "invoice": invoice,
        "booking": booking,
        "car": car
    }

    return render(request, "service/invoice.html", context)
