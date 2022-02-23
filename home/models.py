from distutils.command.upload import upload
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=255)
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
    qty = models.IntegerField()
    def Meta():
        db_table = "products"


