from django.shortcuts import render,redirect
import random
from .models import Cards,User
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib import auth,messages
# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        obj = authenticate(username=username,password=password)
        if obj is not None:
            auth.login(request,obj)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Login Success')
            return redirect('/dashboard')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Invalid Credentials')
            return redirect('/')
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Invalid Request')
    return redirect('/')    
        
def register(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        email=request.POST["email"]
        username=request.POST["username"]
        password=request.POST["password"]
        branch=request.POST["branch"]
        obj = User.objects.create_user(first_name=first_name,email=email,username=username,password=password,branch=branch)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Registration Successful')
        return redirect('/')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request')
        return redirect('/')        

def dashboard(request):
    return render(request,"dashboard.html")

def logout(request):
    auth.logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Logout Successful')
    return redirect('/')

def coupon(request):
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