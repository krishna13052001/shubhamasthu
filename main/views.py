from django.shortcuts import render,redirect
import random
from .models import User,Coupon,Cards,SiteAnnouncements
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib import auth,messages
import secrets
from twilio.rest import Client
import os
import pickle
# Creates your views here.
def get_pickle():
    open_file = open(os.getcwd()+"/main/lucky.pkl", "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list

def save_pickle(arr):
    open_file = open(os.getcwd()+"/main/lucky.pkl", "wb")
    random.shuffle(arr)
    pickle.dump(arr,open_file)
    open_file.close()

def lucky_draw():
    amount_list = get_pickle()
    val = random.choice(amount_list)
    amount_list.remove(val)
    if len(amount_list)==0:
        amount_list = [1000,500]+ [250]*2 + [100]*5 + [50]*10+[25]*181
    save_pickle(amount_list)
    return val

def home(request):
    announcement = SiteAnnouncements.objects.all()
    return render(request,'home.html',{'announcement':announcement})

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
        link = None
        try:
            name=request.POST["name"]
            bill_id = request.POST["bill_id"]
            # email = request.POST["email"]
            mobile = request.POST["mobile"]
            bill_amount = eval(request.POST["bill_amount"])
            # no_of_coupons = request.POST["no_of_coupons"]
            no_of_coupouns = int(bill_amount)//1000
            link = secrets.token_hex(10)
            obj = Coupon.objects.create(name=name,bill_id=bill_id,mobile=mobile,bill_amount=bill_amount,no_of_coupons=no_of_coupouns,created_by=request.user,link=link)
            obj.save()
            for i in range(0,int(no_of_coupouns)):
                string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
                code = ''.join([random.choice(string) for i in range(0,10)])
                while len(Cards.objects.filter(coupon__link=code))>0:
                    code = ''.join([random.choice(string) for i in range(0,10)])
                #amount = random.randint(1,50)
                amount = lucky_draw()
                #code = 'SS'+str(amount)
                obj1 = Cards.objects.create(code=code,amount=amount)
                obj.cards.add(obj1)
                obj.save()
            a = 'AC9d34ee7c820fc8c130178b93d3ea8f3f'#sathya krishna
            b = 'b90312976b5b536413b295027a9a91d9'#sathya krishna
            client = Client(a,b)    
            client.messages.create(body='Dear Sir/Madam,\n\tThank you for shopping with Shubhamasthu Shopping Mall. Click this link to redeem shubhamasthu.herokuapp.com/scratch/'+obj.link,from_='+19093216268',to='+91'+str(mobile))
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Coupons Created and Shared Successfully')
            return redirect('/dashboard')
        except Exception as e:
            Coupon.objects.get(link=link).delete()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,e)
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
            for card in item.cards.all():
                coupon_code+=card.code+','
                total_amount+=card.amount
                if card.scratched==True:
                    scratched_codes+=card.code+','
                else:
                    unscratched_codes+=card.code+','
                if card.redeemed==True:
                    redeemed_codes+=card.code+','
                    redeemed_dates+=card.redeemed_date.strftime("%d-%m-%Y %H:%M:%S")+','
                else:
                    unredeemed_codes+=card.code+','
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
            total = 0
            n = 0
            for item in cards:
                n += 1
                total += item.amount
            return render(request,'displayCard.html',{'cards':cards,'total':total,'n':n})

def cardScratched(request,id):
    obj = Cards.objects.get(id=id)
    obj.scratched = True
    obj.save()
    return render(request,'card.html',{'obj':obj})

def redeem(request):
    if request.method=="POST":
        option = request.POST["option"]
        if option=="0":
            link = request.POST["link"]
            obj = Cards.objects.filter(coupon__link=link,redeemed=False).all().select_related()
            total = 0
            for item in obj:
                total += item.amount
            return render(request,'redeem.html',{'obj':obj,'total':total})
        elif option=="1":
            bill_id = request.POST['bill_id']
            obj = Cards.objects.filter(coupon__bill_id=bill_id,redeemed=False).all().select_related()    
            total = 0
            for item in obj:
                total += item.amount
            return render(request,'redeem.html',{'obj':obj,'total':total})
        elif option=="2":
            mobile = request.POST['mobile']
            obj = Cards.objects.filter(coupon__mobile=mobile,redeemed=False).all().select_related()   
            total = 0
            for item in obj:
                total += item.amount
            return render(request,'redeem.html',{'obj':obj,'total':total})
    return render(request,'redeem.html')

def markRedeem(request):
    if request.method=="POST":
        my_vals = request.POST.getlist("list[]")
        for item in my_vals:
            Cards.objects.filter(id=item).update(redeemed=True,redeemed_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Selected Coupons are redeemed')
        return redirect('/dashboard')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Operation Not allowed')    
        return redirect('/')