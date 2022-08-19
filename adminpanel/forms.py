from django import forms
from accounts.models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password'
    })) #for password field

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Re-enter Password'
    })) #for password field


    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


    def __init__(self,*args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs) #super helps in modifying the way class behaves according to our need(rather than default django way)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' #loop through all fields and give form control


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match!!")


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'Invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'