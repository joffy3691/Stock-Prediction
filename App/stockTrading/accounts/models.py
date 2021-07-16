from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE 
import datetime

# Create your models here.
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    balance = models.FloatField(default=0)

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default = datetime.datetime.now())

class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    stock = models.CharField(max_length=20)
    amount = models.FloatField(default=0)
    current_value = models.FloatField(default=0)
    quantity = models.FloatField()
    date = models.DateTimeField(default = datetime.datetime.now())
    last_updated = models.DateTimeField(default = datetime.datetime.now())
    type = models.CharField(max_length=4)
    is_open = models.BooleanField(default=True)
    open_price = models.FloatField()
    target = models.FloatField()
    trailing_sl = models.FloatField()
    close_price = models.FloatField(null=True)

class Stock(models.Model):
    stock = models.CharField(max_length=20)
    ltp = models.FloatField()
    last_updated = models.DateTimeField(default = datetime.datetime.now())