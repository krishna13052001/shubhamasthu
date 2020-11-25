from django.db import models

# Create your models here.
class Cards(models.Model):
    email = models.EmailField()
    amount = models.IntegerField()