from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cust_name', 'phone', 'address_detail', 'tambon', 'amphoe', 'city', 'postal_code',]
