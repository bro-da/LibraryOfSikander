
from django import forms

from store.models import Product, Variation




class ProductForm(forms.ModelForm):
    images = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ['product_name','description','price','is_available','stock','category','images']

    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)

        self.fields['product_name'].widget.attrs['placeholder']='Enter Product name'
        self.fields['product_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['product_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Product discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3

        self.fields['price'].widget.attrs['placeholder']='Enter Product Price'
        self.fields['price'].widget.attrs['class']='form-control form-control-user'
        self.fields['price'].widget.attrs['type']='text'

        self.fields['stock'].widget.attrs['placeholder']='Enter Product Stock'
        self.fields['stock'].widget.attrs['class']='form-control form-control-user'
        self.fields['stock'].widget.attrs['type']='text'


        self.fields['category'].widget.attrs['class']='form-control form-control-user'


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product','variation_category','variation_value','is_active']