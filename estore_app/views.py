import random
import string
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Order
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

context={}
categories = Product.CAT
context['categories']=categories
p=Product.objects.filter(is_active=True)
context['products']=p

# Create your views here.

def home(request):
    # userid=request.user.id
    # print("Logged-in UserId is: ", userid)
    # print(request.user.is_authenticated)
    # context={}
    p=Product.objects.filter(is_active=True)
    # print(p)
    context['products']=p
    return render(request,'index.html',context)

def product(request,pid):
    p=Product.objects.get(id=pid)
    context['products']=p
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    return render(request, 'product.html', context)

def register(request):
    if request.method == 'POST':
        uemail = request.POST['uemail']
        upass = request.POST['upass']
        cpass = request.POST['cpass']
        context={}
        if uemail == "" or upass == "" or cpass == "":
            context['errmsg'] = "Fields cannot be empty"
        elif upass != cpass:
            context['errmsg'] = "Password and Confirm password didn't match...!!!"
        else:
            try:
                u=User.objects.create(password=upass,username=uemail,email=uemail)
                u.set_password(upass)
                u.save()
                context['success'] = "User created sucessfully"
            except:
                context['errmsg'] = "Username already exists...!!!"
        return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')
    
def user_login(request):
    if request.method == 'POST':
         uemail = request.POST['uemail']
         upass = request.POST['upass']
         context={}
         if uemail == "" or upass == "":
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'login.html', context)
         else:
             u=authenticate(username=uemail,password=upass)
             if u is not None:
                 login(request,u)
                 return redirect('/')
             else:
                 context['errmsg'] = "Invalid username and password"
                 return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    context['products']=p
    return render(request,'index.html', context)

def prodfilter(request):
    psearch=request.GET['psearch']
    q1=Q(name__icontains=psearch)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1 & q2)
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if(request.user.is_authenticated):
        userid=request.user.id
        u=User.objects.get(id=userid)
        q1=Q(uid=u)
        q2=Q(is_deleted=False)
        o=Order.objects.filter(q1 & q2)
        print(o)
        n=len(o)
        print(n)
        if n>0:
            context['errmsg'] = "Order already exists for the User!!!"
        else:
            #q3=Q(is_active=False)
            p=Product.objects.filter(is_active=True)        
            p=Product.objects.get(id=pid)
            context['products']=p
            keys_to_remove = ['success', 'errmsg']
            for key in keys_to_remove:
                context.pop(key, None) 
            #Check product exists or not
            #q1=Q(uid=u)
            q4=Q(pid=p)
            c=Cart.objects.filter(q1 & q4)
            n=len(c)
            if n==1:
                context['errmsg'] = "Product already exists in cart!!!"
            else:
                c=Cart.objects.create(uid=u,pid=p)
                c.save()
                context['success'] = "Product added sucessfully"
        return render(request,'product.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    c=Cart.objects.filter(uid=request.user.id)
    n=len(c)
    total_price = sum(item.pid.price*item.qty for item in c)
    context['product_count']=n
    context['total_price']=total_price
    context['products']=c
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,cid,qv):
    c=Cart.objects.get(id=cid)
    if qv == '1':
        c.qty += 1
    elif qv == '0' and c.qty > 1:
        c.qty -= 1
    else:
        c.qty = 1
    c.save()
    return redirect('/viewcart')

def placeorder(request):
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    c=Cart.objects.filter(uid=request.user.id)
    try:
        order_id = context['order_id']
        print('order_id is:',order_id)
        if order_id is None:
            order_id = generate_order_id()
        print('order_id is:',order_id)
    except:
        order_id = generate_order_id()
        context['order_id catch']=order_id

    for x in c:
        o=Order.objects.create(uid=x.uid,pid=x.pid,qty=x.qty,order_id=order_id)
        o.save()
        x.delete()
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    o=Order.objects.filter(q1 & q2)
    n=len(o)
    total_price = sum(item.pid.price*item.qty for item in o)
    context['product_count']=n
    context['total_price']=total_price
    context['orders']=o
    return render(request,'placeorder.html',context)

def generate_order_id(length=10):
    # Define the characters: uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    # Generate a random alphanumeric string
    order_id = ''.join(random.choices(characters, k=length))
    return order_id

def removeorder(request,oid):
    o=Order.objects.filter(id=oid)
    o.delete()
    return redirect('/placeorder')

def makepayment(request):  
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    o=Order.objects.filter(q1 & q2)
    
    total_price = sum(item.pid.price*item.qty for item in o)

    context['data']=[]
    try:
        client = razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
        data = { "amount": total_price*100, "currency": "INR", "receipt": o[0].order_id }
        payment = client.order.create(data=data)
        context['data']=payment
    finally:
        for x in o:
            x.is_deleted = True
            x.save()
        keys_to_remove = ['order_id']
        for key in keys_to_remove:
            context.pop(key, None) 
        return render(request, 'pay.html', context)

def sendusermail(request):
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    uemail=request.user.email
    #print(uemail)
    #msg= "Order details are: \n Order ID- " + response.razorpay_order_id + "\n Payment ID- " + response.razorpay_payment_id + "Signature-"+response.razorpay_signature
    send_mail(
        "Estore order placed successfully",
        "Order details are",
        "soniyakamble.09@gmail.com",
        [uemail],
        fail_silently=False,
    )
    return render(request,"thanks.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def thanks(request):
    return render(request,"thanks.html")

# def placeorder(request):
#     keys_to_remove = ['success', 'errmsg']
#     for key in keys_to_remove:
#         context.pop(key, None) 
#     o=Order.objects.filter(uid=request.user.id)
#     n=len(o)
#     total_price = sum(item.pid.price for item in o)
#     context['product_count']=n
#     context['total_price']=total_price
#     context['orders']=o
#     return render(request,'cart.html',context)