from django.contrib import admin
from .models import Cards,User
# Register your models here.
class CardUser(admin.ModelAdmin):
    list_display = ['email','amount']
    list_filter = ['email','amount']

admin.site.register(Cards,CardUser)
admin.site.register(User)