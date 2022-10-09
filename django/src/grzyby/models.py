from email.policy import default
from django.db import models

# Create your models here.

class Grzyby(models.Model):
    nameOfShroom = models.CharField(max_length=100)
    descriptionOfShroom = models.CharField(max_length=200)
    picker = models.CharField(max_length=200)
    create_time = models.DateTimeField('create time')
    weightOfShroom = models.IntegerField()
