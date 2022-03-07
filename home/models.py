from distutils.command.upload import upload
import email
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=255)
    productDesc = models.TextField(max_length=1000,null=True)
    productPrize = models.CharField(max_length=255)
    productImage = models.ImageField(upload_to='images/')
    def Meta():
        db_table = "products"


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    productId = models.IntegerField(editable=False, null=True)
    productName = models.CharField(max_length=255)
    productPrize = models.CharField(max_length=255)
    productImage = models.ImageField()
    userId = models.IntegerField(editable=False)
    userName = models.CharField(max_length=255)
    userEmail = models.EmailField(max_length=255, null=True)
    qty = models.IntegerField(default=1, null=True)
    orderId = models.IntegerField(null=True)
    def Meta():
        db_table = "products"


class Orders(models.Model):
    orderId = models.AutoField(primary_key=True)
    order_json = models.TextField(max_length=5000)
    userId = models.IntegerField(editable=False)
    userName = models.CharField(max_length=255)
    userEmail = models.EmailField(max_length=255, null=True)
    userAddress = models.CharField(max_length=555, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zip_code = models.IntegerField(null=True)
    phone = models.BigIntegerField(null=True)
    totalAmount = models.IntegerField(null=True)
    paymentStatus = models.CharField(max_length=255,default='PENDING',null=True)

class ContactUs(models.Model):
    cID = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField(max_length=5000)

