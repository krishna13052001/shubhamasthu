from django.shortcuts import render,redirect
import random
from .models import User,Coupon,Cards
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib import auth,messages
import secrets
from twilio.rest import Client
# Creates your views here.
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

def addCoupon(request):
    if request.method=="POST":
        name=request.POST["name"]
        bill_id = request.POST["bill_id"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        bill_amount = request.POST["bill_amount"]
        no_of_coupons = request.POST["no_of_coupons"]
        obj = Coupon.objects.create(name=name,bill_id=bill_id,email=email,mobile=mobile,bill_amount=bill_amount,no_of_coupons=no_of_coupons,created_by=request.user,link=secrets.token_hex(10))
        obj.save()
        for i in range(0,int(no_of_coupons)):
            amount = random.randint(1,50)
            code = 'SS'+str(amount)
            obj1 = Cards.objects.create(code=code,amount=amount)
            obj.cards.add(obj1)
            obj.save()
        a = 'ACcabcfe0b21027a19fc04e23a660b7215'
        b = 'b231dd874c2a8b7fcc2979269849c42a'
        client = Client(a,b)    
        client.messages.create(body='Dear Sir/Madam,\n\tThank you for shopping with Shubhamasthu Shopping Mall. Click this link to redeem shubhamasthu.herokuapp.com/scratch/'+obj.link,from_='+12512775112',to='+91'+str(mobile))
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Coupons Created and Shared Successfully')
        return redirect('/dashboard')
    return render(request,'addCard.html')

def validateCoupon(request):
    if request.method=="POST":
        option = request.POST["option"]
        if option=="0":
            link = request.POST["link"]
            obj = Cards.objects.filter(coupon__link=link).all().select_related()    
            return render(request,'validateCoupon.html',{'obj':obj})
        elif option=="1":
            bill_id = request.POST['bill_id']
            obj = Cards.objects.filter(coupon__bill_id=bill_id).all().select_related()    
            return render(request,'validateCoupon.html',{'obj':obj})
        elif option=="2":
            mobile = request.POST['mobile']
            obj = Cards.objects.filter(coupon__mobile=mobile).all().select_related()    
            return render(request,'validateCoupon.html',{'obj':obj})
    return render(request,'validateCoupon.html')

import csv
from django.http import HttpResponse
from datetime import datetime
def downStats(request):
    if request.method=="POST":
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        obj = Coupon.objects.filter(date_created__range=(from_date,to_date),created_by__branch=request.user.branch)
        response = HttpResponse(content_type='text/csv')
        file_name = request.user.branch+'-'+request.user.username+'-'+datetime.now().strftime("%d-%m-%Y %H-%M-%S")+'-Coupon Report.csv'
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Bill ID', 'Email', 'Mobile','No of Coupons', 'Bill Amount',
                        'Branch Created','Time','Total Coupon Codes','Amount',
                        'Scratched Codes','Unscratched Codes','Redeemed Codes','Redeemed Dates','Not Redeemed Codes'])
        for item in obj:
            coupon_code,total_amount = '',0
            scratched_codes,unscratched_codes='',''
            redeemed_codes,unredeemed_codes='',''
            redeemed_dates = ''
            print(item.cards)
            for card in item.cards.all():
                coupon_code+=card.code+','
                total_amount+=card.amount
                if card.scratched==True:
                    scratched_codes+=card.code
                else:
                    unscratched_codes+=card.code
                if card.redeemed==True:
                    redeemed_codes+=card.code
                    redeemed_dates+=card.redeemed_date
                else:
                    unredeemed_codes+=card.code
            writer.writerow([item.name,item.bill_id,item.email,item.mobile,item.no_of_coupons,item.bill_amount,item.created_by.branch,item.date_created,
            coupon_code,total_amount,scratched_codes,unscratched_codes,redeemed_codes,redeemed_dates,unredeemed_codes])
        return response
    return render(request,"downStats.html")

def scratch(request,token):
        cards = Cards.objects.filter(coupon__link=token)
        if len(cards)==0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'error')
            return redirect('/')        
        else:
            return render(request,'displayCard.html',{'cards':cards})