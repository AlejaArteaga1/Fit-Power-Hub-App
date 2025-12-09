from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Order, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'price', 'category', 
            'main_category', 'image', 'stock', 'protein_per_serving',
            'carbs_per_serving', 'fat_per_serving', 'calories_per_serving',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative")
        return stock

class CheckoutForm(forms.ModelForm):
    same_as_shipping = forms.BooleanField(
        required=False,
        label='Use same address for billing',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address', 'notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Additional notes...'}),
        }
        labels = {
            'shipping_address': 'Shipping Address',
            'billing_address': 'Billing Address',
            'notes': 'Order Notes',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        same_as_shipping = cleaned_data.get('same_as_shipping')
        shipping_address = cleaned_data.get('shipping_address')
        billing_address = cleaned_data.get('billing_address')
        
        if same_as_shipping and shipping_address:
            cleaned_data['billing_address'] = shipping_address
        
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'gender', 'height', 'weight', 'fitness_goal']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fitness_goal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Lose weight, Gain muscle...'}),
        }
        labels = {
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
            'fitness_goal': 'Fitness Goal',
        }
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height and (height < 50 or height > 250):
            raise forms.ValidationError("Invalid height")
        return height
    
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight and (weight < 20 or weight > 300):
            raise forms.ValidationError("Invalid weight")
        return weight