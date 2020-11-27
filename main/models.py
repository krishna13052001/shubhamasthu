from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    branch = models.CharField(max_length=10,choices=(('Tirupati','Tirupati'),('Nellore','Nellore'),('Vijayawada','Vijayawada')))

class Cards(models.Model):
    email = models.EmailField()
    amount = models.IntegerField()

