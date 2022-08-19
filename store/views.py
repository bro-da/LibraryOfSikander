
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from carts.views import cart
from .models import Product
from .models import Category
from django.db.models import Q
from carts.models import Cart,Cartitem
from carts.views import _cart_id
# Create your views here.
def produ(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug )
        in_cart=Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    products=Product.objects.all().filter(is_available=True)
    categories=Category.objects.all()
   
    Products=None
    

    context ={
        'single_product':single_product,
        'products':products,
        'categories':categories,
        'in_cart':in_cart,
    }
    return render(request,'store/productd.html',context)


def store(request,category_slug=None):
    categories=None
    products=None
    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products= Product.objects.filter(category=categories,is_available=True)
        product_count=products.count
    else:

        products=Product.objects.all().filter(is_available=True)
        product_count=products.count()

    context={
        'products':products,
        'product_count':product_count,

    }
    return render(request,'store/store.html',context)


def search(request):
    products=None
   
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        
        if keyword !=0:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            context={
            'products':products,
            'products_count':products.count,
        }
        
    else:
        
            products=Product.objects.order_by('-created_date')
            context={
            'products':products,
            'products_count':products.count,
            }

    return render(request,'store/store.html',context)


