
from store.models import Product,Category
# Create your views here.
from .models import Account,UserProfile

from django.shortcuts import get_object_or_404, render,redirect


import requests

from orders.models import Order
from django.contrib import messages
from .forms import RegistrationForm,UserProfileForm,UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from carts.models import Cart, Cartitem
from carts.views import _cart_id
from orders.models import OrderProduct
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.utils.encoding import force_bytes


def index(request):
    products=Product.objects.all().filter(is_available=True)
    categories=Category.objects.all()
   
    Products=None
    cproduct=Product.objects.filter(category__slug='childrens')
    context={
        'products':products,
        'categories':categories,
        'cproducts':cproduct,
    }
    return render(request,'base/index.html',context)

def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:
        if  request.method =='POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            user = authenticate(request,email=email,password=password)

            if user is not None:
                try:
                    print('entered the try block')
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=Cartitem.objects.filter(cart=cart).exists()  
                    if is_cart_item_exists:
                        print('entred the if statement')
                        cart_item=Cartitem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user=user
                            item.save()
                except:
                    print('entered tle except block')
                    pass
                login(request,user)
                messages.success(request,'you are logged in')
                url=request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    
                    #next=/carts/checkouts
                    params= dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                        return redirect('index')
                 
            else:
                messages.warning(request,"user name or password is invalid")
                return redirect('loginpage')

        context={}
        return render(request,'accounts/loginpage.html',context)




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            phone_number  = form.cleaned_data['phone_number']
            email  = form.cleaned_data['email']
            password  = form.cleaned_data['password']
            username=email.split("@")[0]
            user= Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phone_number=phone_number
            user.save()
            
            #USER ACTIVATION

            current_site = get_current_site(request)
            mail_subject = 'Please active your account'
            message = render_to_string('account_verification_email.html',{
                'user' : user,
                'domain' : current_site,
                
                
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send() 
            
            request.session['phone_number']=phone_number
            messages.success(request,'Registration successful')
            return redirect('accounts/loginpage')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request,'accounts/register.html',context)

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name  = form.cleaned_data['last_name']
#             phone_number  = form.cleaned_data['phone_number']
#             email  = form.cleaned_data['email']
#             password  = form.cleaned_data['password']
#             username=email.split("@")[0]
#             user= Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
#             user.phone_number=phone_number
#             user.save()
#             messages.success(request,'Registration successful')
#             return redirect('register')
#     else:
#         form = RegistrationForm()
#     context = {
#         'form': form,
#     }
#     return render(request,'accounts/register.html',context)


@login_required(login_url='loginpage')
def logoutUser(request):
    logout(request)
    return redirect('loginpage')



@login_required(login_url='loginpage')
def userdash(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True, status = 'New')
    orders_count = orders.count()
    UserProfile.objects.get_or_create(user=request.user)
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    # order_item=OrderProduct.objects.get(id=request.POST['Product_name'])
    context = {
        'orders_count':orders_count,
        'userprofile' : userprofile,
        'orders' : orders,
        
        
    }
    return render(request, 'accounts/userdash.html', context)

def editprofile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'accounts/editprofile.html', context)




def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'order_detail' : order_detail,
        'order' : order,
        'subtotal' : subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)





def cancel_order(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Cancelled'
    order.save()

    # mail_subject = 'Hey There!. Your order has been cancelled!'
    # mail_subject = 'Order Cancelled'
    # message = render_to_string('orders/order_cancelled_email.html',{
    #     'user':request.user,
    #     # 'order':order,
    #     # 'domain':current_site,
    #     # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #     # 'token':default_token_generator.make_token(user)
    # })
    # to_email = request.user.email
    # print(to_email)
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    # send_email.send()

    messages.success(request, 'Cancellation email has been sent to your email address')
    return render(request,'accounts/userdash.html')
    




