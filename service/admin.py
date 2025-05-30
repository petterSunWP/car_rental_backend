from django.contrib import admin

# Register your models here.
from .models import Car,Booking,Payment,Invoice

admin.site.register(Car)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Invoice)