from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'email', 'phone', 'notes',
                  'address', 'payments', 'delivery', 'city_name']
