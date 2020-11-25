from django.shortcuts import render,redirect
import random
from .models import Cards
from django.core.mail import send_mail
# Create your views here.
def home(request):
    amount = random.randint(5,50)
    if request.method=="POST":
        amount2 = request.POST["amount"]
        email = request.POST["email"]
        Cards.objects.create(amount=amount2,email=email)
        msg= 'Thanks for your Shopping Shubhamasthu. You have received Rs. '+amount2+' in this work.\nThank you for shopping with us '
        send_mail("Shubhamasthu Event Gift Voucher",msg,from_email='adityaintern11@gmail.com',recipient_list=[email])    
        return redirect('/thanks')
    return render(request,'card.html',{'amount':amount})

def thanks(request):
    return render(request,"thanks.html")