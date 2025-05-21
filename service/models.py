from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[("Customer", "Customer"), ("Admin", "Admin")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    mileage = models.IntegerField()
    available_now = models.BooleanField(default=True)
    daily_rental_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Booking(models.Model):
    user_id = models.IntegerField() 
    car_id = models.IntegerField() 
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    booking_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Pending", "Pending"), ("Failed", "Failed")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Issued", "Issued"), ("Paid", "Paid")])
