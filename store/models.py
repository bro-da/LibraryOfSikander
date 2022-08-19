



# Create your models here.
from category.models import Category
from django.urls import reverse
from django.db import models
from django.forms import SlugField


# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug        =models.SlugField(max_length=200,unique=True)
    description =models.TextField(max_length=500,blank=True) 
    price       =models.IntegerField()
    images      =models.ImageField(upload_to='photos/products')    
    stock       =models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('products_by_main_category',args=[self.slug])

    def get_urls(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def get_products(self):
     return self.objects.filter(categories__title=self.category.title)

class VariationManager(models.Manager):
    def booktype(self):
        return super(VariationManager, self).filter(variation_category='booktype', is_active=True)
    def editions(self):
        return super(VariationManager, self).filter(variation_category='editions', is_active=True)

        

    


variation_category_choice = {
    ('booktype','booktype'),
    ('editions','editions'),
}


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'products',max_length = 225)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery' 
