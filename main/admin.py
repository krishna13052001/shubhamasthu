from django.contrib import admin
from .models import Cards
# Register your models here.
class CardUser(admin.ModelAdmin):
    list_display = ['email','amount']
    list_filter = ['email','amount']

admin.site.register(Cards,CardUser)