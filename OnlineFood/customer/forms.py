from django import forms
from customer.models import Customer,Order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
