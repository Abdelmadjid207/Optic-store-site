from typing import Any, Dict, Mapping, Optional, Type, Union
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Client, Seller, Product, Category, Brand
from django.forms import DateInput
from django.http import HttpResponse
import phonenumber_field
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, RegexValidator


class Signupform(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    #first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'first name'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
        
class addclientForm(forms.ModelForm):

    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name of the customer'}), required=True)
    last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last/Family name of the customer'}), required=True)
    birthdate = forms.DateField(label="Birth Date", required=True, widget=forms.DateInput(format='%d/%m/%Y',attrs={'class':'form-control', 'format':'%d/%m/%Y', 'placeholder':'dd/mm/yyyy'}), input_formats=('%d/%m/%Y' ,), validators=[MaxValueValidator(datetime.date.today())])
    added_at = forms.DateTimeField(label="Last update", required=True, initial=datetime.datetime.now,  widget=forms.HiddenInput())
    last_update = forms.DateTimeField(label="Last update", required=True, initial=datetime.datetime.now,  widget=forms.HiddenInput())
    gender = forms.ChoiceField(label="Gender", required=True, choices=Client.GENDERR, widget=forms.Select(attrs={'class':'form-control'}))
    face_shape = forms.ChoiceField(label="Face shape", required=True, choices=Client.SHAPES, widget=forms.Select(attrs={'class':'form-control'}))
    eye_color = forms.ChoiceField(label="Eye color", required=True, choices=Client.ECOLOR, widget=forms.Select(attrs={'class':'form-control'}))
    skin_color = forms.ChoiceField(label="Skin Tone", required=True, choices=Client.SKINT, widget=forms.Select(attrs={'class':'form-control'}))
    phone_number = forms.CharField(label="Phone number",  widget= forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Phone number of the customer', 'size':'10'}), required=True, validators=[RegexValidator(regex=r'^(06|07|05)',message='The first two digits must be 06, 07, or 05.',),])
    added_by = forms.CharField(widget=forms.HiddenInput(), required=False)
    edited_by = forms.CharField(widget=forms.HiddenInput(), required=False)
    total = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Client
        exclude =("user", )

        
    

class addsellerForm(forms.ModelForm):
    first_sname = forms.CharField(label="First name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name of the seller'}), required=True)
    last_sname = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last/Family name of the seller'}), required=True)
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email of the seller'}), required=True)
    phones_number = forms.DecimalField(label="Phone number", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone number of the seller'}), required=True)
    added_by = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Seller
        exclude =("user",)


class addproductForm(forms.ModelForm):
    category = forms.ModelChoiceField(label="Select Category", widget=forms.Select(attrs={'class':'form-control'}), queryset=Category.objects.all().order_by('name'))
    brand = forms.ModelChoiceField(label="Select Brand", widget=forms.Select(attrs={'class':'form-control'}), queryset=Brand.objects.all().order_by('name'))
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of the product. You can specify it by adding color ... etc'}), required=True)
    seller = forms.ModelMultipleChoiceField(label="Select seller", widget=forms.CheckboxSelectMultiple, queryset=Seller.objects.all())
    price = forms.DecimalField(label="Price", decimal_places=2, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Product\'s price'}), required=True)
    quantity = forms.DecimalField(label="Quantity", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Product\'s quantity'}), required=True)
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Infos about the product. Ex: Type, Wear time ... etc'}), required=False)
    barcode = forms.DecimalField(label="Codebar", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Product\'s barcode'}), required=True)
    added_by = forms.CharField(widget=forms.HiddenInput(), required=False)
    status = forms.CharField(widget=forms.HiddenInput(), required=False)
    added = forms.DateField(widget=forms.HiddenInput(), initial=datetime.date.today, required=False)
    class Meta:
        model = Product
        exclude =("user",)
        



    