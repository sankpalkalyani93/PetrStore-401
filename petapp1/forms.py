from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import PetUser, Pet, Product, Contact
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Remember Me")

class PetUserForm(UserCreationForm):
    class Meta:
        model = PetUser
        fields = ['username', 'fname', 'lname', 'email1', 'phone1', 'address1', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(PetUserForm, self).__init__(*args, **kwargs)
        
        # Apply max_length and Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Explicitly set max_length for password fields
        self.fields['password1'].widget.attrs.update({'maxlength': '100'})
        self.fields['password2'].widget.attrs.update({'maxlength': '100'})

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'price', 'type', 'description', 'image']        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)

        # Explicitly styling the ImageField
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'quantity_in_stock', 'description', 'image']        
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Explicitly styling the ImageField
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
            
        }