from django import forms
from restaurant.models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['res_name','min_order','location','status','approved']