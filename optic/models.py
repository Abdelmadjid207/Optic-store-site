from django.db import models
from django.conf import settings
from django.http import HttpResponse
import datetime
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class Client(models.Model):
    ROUND = 'Round'
    SQUARE = 'Square'
    TRIANGLE = 'Triangle'
    OVAL = 'Oval'
    HEART = 'Heart'
    SHAPES = [
        (ROUND, ('Round')),
        (SQUARE, ('Square')),
        (TRIANGLE, ('Triangle')),
        (OVAL, ('Oval')),
        (HEART, ('Heart')),
    ]
    
    MALE = 'Male'
    FEMALE = 'Female'
    GENDERR = [
        (MALE, ('Male')),
        (FEMALE, ('Female')),
    ]
    
    AMBER = 'Amber'
    BLUE = 'Blue'
    BROWN = 'Brown'
    GRAY = 'Gray'
    GREEN = 'Green'
    HAZEL = 'Hazel'
    RED = 'Red'
    ECOLOR = [
        (AMBER, ('Amber')),
        (BLUE, ('Blue')),
        (BROWN, ('Brown')),
        (GRAY, ('Gray')),
        (GREEN, ('Green')),
        (HAZEL, ('Hazel')),
        (RED, ('Red')),          
    ]
    
    PALE = 'Pale'
    FAIR = 'Fair'
    MEDIUM = 'Medium'
    OLIVE = 'Olive'
    BR = 'Brown'
    DARK = 'Dark'
    SKINT = [
        (PALE, ('Pale')),
        (FAIR, ('Fair')),
        (MEDIUM, ('Medium')),
        (OLIVE, ('Olive')),
        (BR, ('Brown')),
        (DARK, ('Dark')),         
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    added_at = models.DateTimeField(default=datetime.datetime.now)
    birthdate = models.DateField(null=True)
    last_update = models.DateTimeField(default=datetime.datetime.now)
    gender = models.CharField(max_length=10, choices=GENDERR)
    face_shape = models.CharField(max_length=10, choices=SHAPES)
    eye_color = models.CharField(max_length=10, choices=ECOLOR)
    skin_color = models.CharField(max_length=10, choices=SKINT)
    phone_number = models.CharField(max_length=10, null=True)
    added_by = models.CharField(max_length=30, null=True)
    edited_by = models.CharField(max_length=30, null=True)
    
    def __str__(self) -> str:
        return (f"{self.first_name} {self.last_name}")
    
class Seller(models.Model):
    first_sname = models.CharField(max_length=100)
    last_sname = models.CharField(max_length=100)
    added = models.DateField(auto_now_add=True)
    added_by = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=100)
    phones_number = models.DecimalField(max_digits=10, decimal_places=0)
    def __str__(self) -> str:
        return (f"{self.first_sname} {self.last_sname}")


class Category(models.Model):
    NADMIN = 'Added by a non-admin user'
    ADMIN = 'Approved by Admin'
    ADDER = [
        (NADMIN, ('Added by a non-admin user')),
        (ADMIN, ('Approved by Admin')),
    ]
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=ADDER, default=NADMIN)

    def __str__(self):
        return (self.name)


class Brand(models.Model):
    NADMIN = 'Added by a non-admin user'
    ADMIN = 'Approved by Admin'
    ADDER = [
        (NADMIN, ('Added by a non-admin user')),
        (ADMIN, ('Approved by Admin')),
    ]
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=ADDER, default=NADMIN)

    def __str__(self):
        return (self.name)


class Product(models.Model):
    NADMIN = 'Added by a non-admin user'
    ADMIN = 'Approved by Admin'
    ADDER = [
        (NADMIN, ('Added by a non-admin user')),
        (ADMIN, ('Approved by Admin')),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    seller = models.ManyToManyField(Seller)
    description = models.CharField(max_length=2000, null=True)
    barcode = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=30, choices=ADDER, default=NADMIN)
    added_by = models.CharField(max_length=30, null=True)
    added = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return (self.name)



class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    desc = models.CharField(max_length=1000, null=True)
    i_quantity = models.IntegerField(default=1)
    updated = models.DateField(null=datetime.date.today)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)










class ActionCounter(models.Model):
    date = models.DateField(null=datetime.date.today)
    count = models.PositiveIntegerField(default=0)

    def increase_count(self):
        self.count += 1
        self.save()
    def decrease_count(self):
        self.count -= 1
        self.save()

class ClientCounter(models.Model):
    date = models.DateField(null=datetime.date.today)
    count = models.PositiveIntegerField(default=0)

    def increase_count(self):
        self.count += 1
        self.save()
    def decrease_count(self):
        self.count -= 1
        self.save()

class SaleCounter(models.Model):
    date = models.DateField(null=datetime.date.today)
    count = models.DecimalField(default=0, decimal_places=2, max_digits=10)


