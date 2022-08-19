from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   path('',views.store,name='store'),
   path('category/<slug:category_slug>/', views.store,name='products_by_category'),
   
   path('produ',views.produ,name='produ'),
   path('produ/<slug:category_slug>/<slug:product_slug>/', views.produ,name='product_detail'),
   path('search/',views.search,name='search'),
   
]