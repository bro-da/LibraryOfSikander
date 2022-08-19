from .models import Category
from wishlist.models import Wishlist,WishlistItem
from django.shortcuts import render,redirect,get_object_or_404
from wishlist.views import _wishlist_id, wishlist
from django.core.exceptions import ObjectDoesNotExist
def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)



# def wishlists(request):
#     wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
#     if request.user.is_authenticated:
#         try:
            
#             wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active = True)

#         except ObjectDoesNotExist:
#             pass
#     else:
#         wishlist_items=wishlist.objects.all()
  
#     return dict(wishlist_itams=wishlist_items)


def wishlists(request,wishlist=0):
    wish_counter=0
    wishlist_itams=None
    if 'admin' in request.path:
        return{}
    else:
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_itams=WishlistItem.objects.filter(wishlist=wishlist, is_active = True),
            if wishlist_itams!=0:
                wish_counter=WishlistItem.objects.filter(wishlist=wishlist, is_active = True).count()
            else:
                wish_counter=0
        except Wishlist.DoesNotExist:
            wish_counter=0
            pass
    return {
       'wishlist_itams':WishlistItem.objects.filter(wishlist=wishlist, is_active = True),
       'wish_counter':wish_counter,
     }


    