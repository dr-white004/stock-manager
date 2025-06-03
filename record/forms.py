# forms.py
from django import forms
from .models import ClockType, Stock, Sale, Return
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username'] 



class ClockTypeForm(forms.ModelForm):
    class Meta:
        model = ClockType
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['clock_type', 'quantity_received', 'defective_quantity']
        
    def clean(self):
        cleaned_data = super().clean()
        quantity_received = cleaned_data.get('quantity_received')
        defective_quantity = cleaned_data.get('defective_quantity', 0)
        
        if defective_quantity > quantity_received:
            raise forms.ValidationError("Defective quantity cannot exceed received quantity")
        
        return cleaned_data

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['clock_type', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['clock_type', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }