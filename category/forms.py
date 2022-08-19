
from django import forms
from .models import Category



 

class CategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model  = Category
        fields = ['category_name','description','cat_image']

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)

        # self.fields['main_category'].widget.attrs['class']='form-control form-control-user'

        self.fields['category_name'].widget.attrs['placeholder']='Enter Category name'
        self.fields['category_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['category_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Category discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3
        
        # self.fields['image'].widget.attrs['placeholder']='Add images'
        # self.fields['image'].widget.attrs['class']='form-control'
        # self.fields['image'].widget.attrs['type']='file'





