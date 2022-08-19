
from django.http import HttpResponse
from django.shortcuts import render,redirect
from carts.models import Cartitem,Cart
from .forms import OrderForms
from .models import Order
import datetime
import razorpay
import json
from .models import OrderProduct,Payment
from store.models import Product
from django.http import JsonResponse
# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['order_id'])
    payment = Payment(
        user = request.user,
        payment_id = body['razorpay_payment_id'],
        amount_paid = body['amount_paid'],
        status = body['status'],
        payment_method = body['payment_method']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    
    cart_items = Cartitem.objects.filter(user=request.user)
# create with create command
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    Cartitem.objects.filter(user=request.user).delete()


    # mail_subject = 'Thank You. Your order has been recieved'
    # message = render_to_string('orders/order_recieved_email.html',{
    #     'user':request.user,
    #     'order':order,
    #     # 'domain':current_site,
    #     # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #     # 'token':default_token_generator.make_token(user)
    # })
    # to_email = request.user.email
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    # send_email.send()


    data = {
        'order_id':order.order_number,
        'payment_id':payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items=Cartitem.objects.filter(user=current_user)
    print(cart_items)
    cart_count=cart_items.count()

    print(cart_count)
    if cart_count<=0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            #generating order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")  #eg-20210505
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            client = razorpay.Client(auth=("rzp_test_1QXaC4gmNQTUQr", "VnCB5LbcWskeMPeIWb3h2Vd3"))
            DATA = {
                'amount' : data.order_total*100,
                'currency' : 'INR',
                'payment_capture' : 1,
            }
        payment = client.order.create(data=DATA)

        print('****')
        print(request.user)
        print('****')
            
        context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
                'payment' : payment,
            }
        return render(request, 'carts/payments.html', context)
    else:
        return redirect('checkout')

        
   


def order_complete(request):
    return render(request, 'store/order_complete.html')


# def payments(request):
#     return render(request,'payments.html')

