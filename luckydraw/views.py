from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Coupon,Cards,CouponCount,Winner
import secrets
import random
import urllib

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    # print(fr)
    return(fr)

def validateMobileNumber(request):
    if request.method=="POST":
        request.session["name"]=request.POST["name"]
        request.session["bill_id"] = str(request.POST["bill_id"])
        request.session["mobile"] = request.POST["mobile"]
        request.session["bill_amount"] = request.POST["bill_amount"]
        string = '0123456789'
        if(int(eval(request.session["bill_amount"]))< 999):
            messages.info(request,"Bill Amount is less than 999")
            return redirect('/luckydraw/dashboard')
        otp = ''.join([random.choice(string) for i in range(0,4)])
        # print(otp)
        request.session["otp"] = otp
        sender='SBMSTU'
        api = 'MWE4M2Y4MGRjY2QzZTRhMDkxOGUxYzhkOGViYTVjZWY='
        sendSMS(apikey=api,sender=sender,numbers='+91'+str(request.session["mobile"]),message=f"Dear Customer, your one time password for Lucky Draw Coupon is {otp} - Subhamasthu Shopping Mall")
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'OTP sent successfully')
        return redirect('/luckydraw/validateOtp')

def validateOtp(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method=="POST":
        try:
            if(request.POST["otp"]==request.session["otp"]):
                request.session["otp"]=None
                return createCoupon(request)
                # return redirect('/luckydraw/dashboard')
            else:
                storage = messages.get_messages(request)
                storage.used = True
                messages.info(request,"OTP is not valid")
                return redirect('/luckydraw/addCoupon')
        except Exception as e:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,e)
            return redirect('/luckydraw/addCoupon')
    return render(request,'luckydraw/validateOtp.html')            

def deleteCoupon(id):
    obj = Coupon.objects.get(id=id)
    obj.delete()

# Create your views here.
def createCoupon(request):
        link = None
        try:
            name=request.session["name"]
            bill_id = str(request.session["bill_id"])
            mobile = request.session["mobile"]
            bill_amount = request.session["bill_amount"]
            no_of_coupouns = eval(bill_amount)//999
            if(no_of_coupouns == 0):
                messages.info(request,"No Coupons were")
                return redirect('/luckydraw/dashboard')
            link = secrets.token_hex(10)
            obj = Coupon.objects.create(name=name,bill_id=bill_id,mobile=mobile,bill_amount=bill_amount,no_of_coupons=no_of_coupouns,lucky_created_by=request.user,link=link)
            obj.save()
            for i in range(0,int(no_of_coupouns)):
                if request.user.branch == "Tirupati":
                    object = CouponCount.objects.all()
                    if len(object)>0:
                        code = object[0].tirupati_count
                        object[0].tirupati_count+=1
                        object[0].save()
                        count = 0
                        while count!=10 and Cards.objects.filter(code='TPT'+str(code).zfill(7)).exists():
                            code = object[0].tirupati_count
                            object[0].tirupati_count+=1
                            object[0].save()
                            count+=1
                        if count==10:
                            storage = messages.get_messages(request)
                            storage.used = True
                            messages.info(request,'Count 10: please try after 5 minutes')
                            deleteCoupon(obj.id)
                            return redirect('/luckydraw/dashboard')    
                        obj1 = Cards.objects.create(code='TPT'+str(code).zfill(7),luckycard_issued_by=request.user)
                        obj.lucky_cards.add(obj1)
                        obj.save()
                elif request.user.branch == "Nellore":
                    object = CouponCount.objects.all()
                    if len(object)>0:
                        code = object[0].nellore_count
                        object[0].nellore_count+=1
                        object[0].save()
                        count = 0
                        while count!=10 and Cards.objects.filter(code='NLR'+str(code).zfill(7)).exists():
                            code = object[0].nellore_count
                            object[0].nellore_count+=1
                            object[0].save()
                            count+=1
                        if count==10:
                            storage = messages.get_messages(request)
                            storage.used = True
                            messages.info(request,'Count 10: please try after 5 minutes')
                            deleteCoupon(obj.id)
                            return redirect('/luckydraw/dashboard')    
                        obj1 = Cards.objects.create(code='NLR'+str(code).zfill(7),luckycard_issued_by=request.user)
                        obj.lucky_cards.add(obj1)
                        obj.save()
                elif request.user.branch == "Vijayawada":
                    object = CouponCount.objects.all()
                    if len(object)>0:
                        code = object[0].vijayawada_count
                        object[0].vijayawada_count+=1
                        object[0].save()
                        count = 0
                        while count!=10 and Cards.objects.filter(code='VJY'+str(code).zfill(7)).exists():
                            code = object[0].vijayawada_count
                            object[0].vijayawada_count+=1
                            object[0].save()
                            count+=1
                        if count==10:
                            storage = messages.get_messages(request)
                            storage.used = True
                            messages.info(request,'Count 10: please try after 5 minutes')
                            deleteCoupon(obj.id)
                            return redirect('/luckydraw/dashboard')
                        obj1 = Cards.objects.create(code='VJY'+str(code).zfill(7),luckycard_issued_by=request.user)
                        obj.lucky_cards.add(obj1)
                        obj.save()
            sender='SBMSTU'
            api = 'MWE4M2Y4MGRjY2QzZTRhMDkxOGUxYzhkOGViYTVjZWY='
            sendSMS(apikey=api,sender=sender,numbers='+91'+str(mobile),message="Dear Customer, Click this link to grab your coupon shubhamasthu.herokuapp.com/scratch/"+obj.link+" - Subhamasthu Shopping Mall.")
            storage = messages.get_messages(request)
            storage.used = True
            request.session["displayCoupon"]=True
            request.session["couponId"] = obj.id
            # print(request.session["displayCoupon"])
            # print(request.session["couponId"])
            messages.info(request,'Coupons Created and Shared Successfully')
            return redirect('/luckydraw/dashboard')
        except Exception as e:
            try:
                Coupon.objects.get(link=link).delete()
            except:
                pass
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,e)
            return redirect('/luckydraw/dashboard')

def addCoupon(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    return render(request,'luckydraw/addCard.html')

def dashboard(request): 
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    displayCoupon = request.session.get("displayCoupon",False)
    coupon_obj = None
    if displayCoupon==True:
        coupon_obj = Coupon.objects.filter(id=request.session["couponId"]).select_related()
        request.session["displayCoupon"]=False
        cards = coupon_obj[0].lucky_cards.all()
        n = len(coupon_obj[0].lucky_cards.all())
        return render(request,'luckydraw/dashboard.html',{"displayCoupon":displayCoupon,"cards":cards,"n":n})
    else:
        return render(request,'luckydraw/dashboard.html',{"displayCoupon":displayCoupon,"cards":None,"n":0})

def scratch(request,token):
        cards = Cards.objects.filter(lucky_cards__link=token)
        # print(len(cards))
        if len(cards)==0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'error')
            return redirect('/luckydraw/dashboard')
        else:
            n = 1
            di = {}
            amount_redeemed = 0
            for item in cards:
                di[n] = item
                n+=1
            return render(request,'luckydraw/displayCard.html',{'cards':di,'n':n-1,'amount_redeemed':amount_redeemed})

def cardScratched(request,id):
    obj = Cards.objects.get(id=id)
    obj.scratched = True
    obj.save()
    return render(request,'luckydraw/card.html',{'obj':obj})

def redeemCoupon(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method=="POST":
        code = request.POST.get('code')
        card_obj = Cards.objects.filter(code=code).select_related()
        if card_obj[0].redeemed == True:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,"Already Redeemed")
            return redirect('/luckydraw/dashboard')
        mobile = card_obj[0].lucky_cards.all()[0].mobile
        string = '0123456789'
        otp = ''.join([random.choice(string) for i in range(0,4)])
        # print(otp)
        request.session["otp"] = otp
        request.session['card_id'] = card_obj[0].id
        sender='SBMSTU'
        api = 'MWE4M2Y4MGRjY2QzZTRhMDkxOGUxYzhkOGViYTVjZWY='
        sendSMS(apikey=api,sender=sender,numbers='+91'+str(mobile),message=f"Dear Customer, your one time password for Lucky Draw Coupon is {otp} - Subhamasthu Shopping Mall")
        return redirect('/luckydraw/redeemotp')
    return render(request,"luckydraw/redeemCoupon.html")
from datetime import datetime
def redeemotp(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method=="POST":
        try:
            if(request.POST["otp"]==request.session["otp"]):
                request.session["otp"]=None
                card_obj = Cards.objects.get(id=request.session["card_id"])
                card_obj.redeemed=True
                card_obj.redeemed_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                card_obj.save()
                storage = messages.get_messages(request)
                storage.used = True
                messages.info(request,"OTP is valid!! Congratulations")
                return redirect('/luckydraw/dashboard')
            else:
                storage = messages.get_messages(request)
                storage.used = True
                messages.info(request,"OTP is not valid")
                return redirect('/luckydraw/dashboard')
        except Exception as e:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,e)
            return redirect('/luckydraw/dashboard')
    return render(request,'luckydraw/redeemotp.html')            

def validateCoupon(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method=="POST":
        option = request.POST["option"]
        if option=="0":
            link = request.POST["link"]
            obj = Cards.objects.filter(lucky_cards__link=link).all().select_related()    
            return render(request,'luckydraw/validateCoupon.html',{'obj':obj})
        elif option=="1":
            bill_id = request.POST['bill_id']
            obj = Cards.objects.filter(lucky_cards__bill_id=bill_id).all().select_related()    
            return render(request,'luckydraw/validateCoupon.html',{'obj':obj})
        elif option=="2":
            mobile = request.POST['mobile']
            obj = Cards.objects.filter(lucky_cards__mobile=mobile).all().select_related()
            # print(obj)
            return render(request,'luckydraw/validateCoupon.html',{'obj':obj})
    return render(request,'luckydraw/validateCoupon.html')

def weekly(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method=="POST":
        code = request.POST.get('code')
        card_obj = Cards.objects.filter(code=code).select_related()
        if card_obj[0].redeemed == True:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,"Already Redeemed")
            return redirect('/luckydraw/dashboard')
        mobile = card_obj[0].lucky_cards.all()[0].mobile
        string = '0123456789'
        otp = ''.join([random.choice(string) for i in range(0,4)])
        # print(otp)
        request.session["otp"] = otp
        request.session['card_id'] = card_obj[0].id
        sender='SBMSTU'
        api = 'MWE4M2Y4MGRjY2QzZTRhMDkxOGUxYzhkOGViYTVjZWY='
        sendSMS(apikey=api,sender=sender,numbers='+91'+str(mobile),message=f"Dear Customer, your one time password for Lucky Draw Coupon is {otp} - Subhamasthu Shopping Mall")
        return redirect('/luckydraw/redeemotp')
    return render(request,'luckydraw/weekly.html')

def daily(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method == "POST":
        pass
    return render(request,'luckydraw/daily.html')

def informCustomer(request):
    if(not request.user.is_authenticated):
        messages.info(request,"Please Login/Register")
        return redirect("/login")
    if request.method == "POST":
        code = request.POST.get('code').strip()[:10]
        card_obj = Cards.objects.filter(code=code).select_related()
        coupon_obj = card_obj[0].lucky_cards.all()[0]
        Winner.objects.create(winner_card=card_obj[0],winner_coupon=coupon_obj)
        mobile = card_obj[0].lucky_cards.all()[0].mobile
        date_var = datetime.now().strftime('%Y-%m-%d')
        sender='SBMSTU'
        api = 'MWE4M2Y4MGRjY2QzZTRhMDkxOGUxYzhkOGViYTVjZWY='
        try:
            sendSMS(apikey=api,sender=sender,numbers='+91'+str(mobile),message=f"Congratulations Dear Customer, You have won the lucky draw of {code} which was drawn on Date {date_var}. Please show this message to the Showroom Manager for further process & conditions apply  - Subhamasthu Shopping Mall")
        except:
            storage.used = True
            storage = messages.get_messages(request)
            messages.info(request,"SMS not sent")
            return redirect('/luckydraw/informCustomer')
        messages.info(request,"Lucky Person informed")
    return render(request,'luckydraw/informCustomer.html')

def displayWinners(request):
    winners = Winner.objects.all().select_related()
    return render(request,"luckydraw/winners.html",{'winners':winners})