from django.contrib import admin
from django.urls import path
from customer import views


urlpatterns = [
    path('',views.about,name='about'),
    path('contact/',views.contactUs,name='contact'),
    path('customer_signup/',views.SignUp.as_view(),name='signup'),
    path('customer_login/',views.Login.as_view(),name='login'),
    path('customer_profile/',views.profile,name='profile'),
	# path('update_profile/',views.UpdateProfile.as_view(),name='update_profile'),
	path('customer_dashboard/',views.dashboard,name='dashboard'),
    path('customer_logout/',views.logout,name='logout'),
    path('food_items/',views.FoodItems.as_view(),name='food_items'),#add to cart
    path('view_cart/',views.Cart.as_view(),name='view_cart'),
	path('delete_cart_item/',views.delete_item,name='delete_cart_item'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
	path('payment/',views.Payment.as_view(),name='payment'),
	path('success/',views.success,name='success'),
    path('order/',views.OrderView.as_view(),name='order'),
]
