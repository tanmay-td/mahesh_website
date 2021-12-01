from functools import total_ordering
from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User


# Create your models here.

class agent(models.Model):
    name =models.CharField(max_length= 50,unique=True)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name



class farmer(models.Model):
    name = models.CharField(max_length= 50,unique=True)
    agent = models.ForeignKey(agent,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    total_balance = models.DecimalField(max_digits=10,decimal_places=2)
    returned = models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    quantity = models.DecimalField(max_digits=10,decimal_places=2)
    rate = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name


class transaction(models.Model):
    name = ForeignKey(farmer,on_delete=models.CASCADE)
    paid = models.DecimalField(max_digits=10,decimal_places=2)
    remark = models.CharField(max_length=50,blank= True)
    date = models.DateTimeField()

    def __str__ (self):
        return str(self.name)