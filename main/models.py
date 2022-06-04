from pickle import TRUE
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PRODUCT_CATEGORIES = (
    ('M', 'Men'),
    ('W', 'Women'),
    ('K', 'Kid'),
    ('A', 'Accessories')
)

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE ,null=TRUE,blank=TRUE)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=TRUE)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    slug = models.SlugField(unique=True)
    category = models.CharField(choices=PRODUCT_CATEGORIES, max_length=2 , null=TRUE,blank=TRUE)
    rating = models.IntegerField(default=0,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    quote = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name

    @property
    def imageurl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=TRUE,null=TRUE)
    date_ordered = models.DateTimeField(auto_now_add=TRUE)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=TRUE,null=TRUE)
    order =  models.ForeignKey(Order,on_delete=models.SET_NULL,null=TRUE,blank=TRUE)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=TRUE)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=TRUE,null=TRUE)
    order =  models.ForeignKey(Order,on_delete=models.SET_NULL,null=TRUE,blank=TRUE)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=TRUE)

    def __str__(self):
        return self.address

