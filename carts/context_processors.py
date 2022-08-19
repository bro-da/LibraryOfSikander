from .models import Cart,Cartitem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            
            if request.user.is_authenticated:
                cart_items=Cartitem.objects.all().filter(user=request.user)
            else:
                cart_items=Cartitem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count+=cart_item.quantity
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)


# my_codes
# def UserCart(request,cart_items=None):
#     try:
            
#         if request.user.is_authenticated:
#                 cart_items=Cartitem.objects.all().filter(user=request.user)
#         else:
#                 cart=Cart.objects.filter(cart_id=_cart_id(request))
#                 cart_items=Cartitem.objects.all().filter(cart=cart[:1])

#     except Cart.DoesNotExist:
#             cart=Cart.objects.filter(cart_id=_cart_id(request))
#             cart_items=Cartitem.objects.all().filter(cart=cart[:1])
        
#     return dict(cart_itams=cart_items)



        
# def UserCart(request,cart_itams=None):
#     if request.user.is_authenticated:
#         cart_itams=Cartitem.objects.all().filter(user=request.user)
#     else:
#         cart=Cart.objects.filter(cart_id=_cart_id(request))
#         cart_itams=Cartitem.objects.all().filter(cart=cart[:1])
#     return dict(cart_itams=cart_itams)


def show_product(request):
    cart = Cart.objects.filter(cart_id = _cart_id(request))
    if request.user.is_authenticated:
        cart_items = Cartitem.objects.all().filter(user=request.user)

    else:
        cart_items = Cartitem.objects.all().filter(cart= cart[:1])
    return dict(show_product = cart_items)