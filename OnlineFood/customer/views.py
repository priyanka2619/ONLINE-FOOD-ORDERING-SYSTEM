import razorpay as razorpay
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View
from customer.models import Customer,Order
from restaurant.models import MenuItem
from django.db.models import Q
from customer.forms import CustomerForm


# Create your views here.
def about(request):
    return render(request,"about.html")

def contactUs(request):
    return render(request,"contact.html")

class SignUp(View):
    def get(self,request):
        cf = CustomerForm()
        return render(request,"customer/signup.html",{"form":cf})

    def post(self,request):
        try:
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            m_no = request.POST.get('mobile_no')
            addrs = request.POST.get('address')
            img = request.FILES.get('image')
            e_mail = request.POST.get('email')
            pass_word = request.POST.get('password')
            pass_word = make_password(pass_word) #hashed password

            customer = Customer(f_name=fname,l_name=lname,phone=m_no,email=e_mail,password=pass_word,address=addrs,image=img)
            customer.save()
            return redirect('login')
        except IntegrityError:
            return render(request,"customer/signup.html",{"error":'Contact no & Email must be unique only'})


class Login(View):
    def get(self,request):
        return render(request,"customer/login.html")

    def post(self,request):
        email_id = request.POST.get("email")
        password = request.POST.get("password")
        try:
            customer = Customer.objects.get(email=email_id)
            decoded_password = check_password(password, customer.password)
            #print(decoded_password)
            if decoded_password:
                request.session["id"] = customer.id
                request.session["name"] = customer.f_name
                request.session["email"] = customer.email
                request.session["contact"] = customer.phone
                return redirect('profile')
            else:
                return render(request, "customer/login.html", {"error": "Invalid Password"})
        except Customer.DoesNotExist:
            return render(request, "customer/login.html", {"error": "Invalid Email"})


def profile(request):
	return render(request,"customer/profile_page.html")

def dashboard(request):
    return render(request,"customer/dashboard.html")

def logout(request):
   request.session.clear()
   return redirect('login')


class FoodItems(View):
	def get(self,request):
		menu = MenuItem.objects.all()
		return render(request, "restaurant/menu_items.html", {"menu_items": menu})

	def post(self,request):
		product_id = request.POST.get("product")
		remove = request.POST.get("remove")
		cart = request.session.get("cart")
		if cart:
			quantity = cart.get(product_id)
			if quantity:
				if remove:
					if quantity <= 1:
						cart.pop(product_id)
					else:
						cart[product_id] = quantity - 1
				else:
					cart[product_id] = quantity + 1
			else:
				cart[product_id] = 1
		else:
			cart = {}
			cart[product_id] = 1

		request.session['cart'] = cart
		print("Cart is ", cart)
		return redirect('menuitems')


class Cart(View):
    def get(self,request):
        ids = request.session.get('cart').keys()
        items = MenuItem.objects.filter(id__in=ids)
        #print(items)
        return render(request,"customer/view_cart.html",{"items":items})

def delete_item(request):
	cart = request.session.get('cart')
	customer_id = request.POST.get('customer_id')
	#print(customer_id)
	if customer_id in cart:
		del cart[customer_id]
		request.session['cart'] = cart
	return redirect('view_cart')

class Checkout(View):
    def get(self,request):
	    ids = request.session.get('cart').keys()
	    items = MenuItem.objects.filter(id__in=ids)
	    return render(request,"customer/checkout.html",{"items":items})

    def post(self,request):
	    b_name = request.POST.get("bname")
	    b_m_no = request.POST.get("bmobile_no")
	    b_adrs = request.POST.get("baddress")
	    s_name = request.POST.get("sname")
	    s_m_no = request.POST.get("smobile_no")
	    s_adrs = request.POST.get("saddress")
        #t_amount = float(request.POST.get("total"))
	    customer_id = request.session.get("id")
	    cart = request.session.get('cart')
	    items = MenuItem.objects.filter(id__in=list(cart.keys()))
	    #print("Items in menu: ",items)
	    for item in items:
	        order = Order(orderedBy=Customer(id=customer_id), menuitem=item, restaurant_id_id=item.restaurant.id, price=item.price, quantity=cart.get(str(item.id)), biling_name=b_name, biling_mno=b_m_no, biling_address=b_adrs, shipping_name=s_name, shipping_mno=s_m_no, shipping_address=s_adrs)
	        order.placeOrder()
	    return render(request,"customer/payment.html")

class Payment(View):
	def get(self,request):
		ids = request.session.get('cart').keys()
		items = MenuItem.objects.filter(id__in=ids)
		return render(request,"customer/payment.html",{"items":items})

	def post(self,request):
		# razorpay
		amount = 300*100
		client = razorpay.Client(auth=('rzp_test_Mx39FX2QV9K5f0', 'PWck8Slw0l3AHRqEVsWmBwF3'))
		data = {'amount': amount, 'currency': 'INR', 'payment_capture': '1'}
		payment = client.order.create(data)
		print("PAYMENT DETAIL: ", payment)
		return render(request,"customer/payment.html")


def success(request):
	ids = request.session.get('cart').keys()
	items = MenuItem.objects.filter(id__in=ids)
	return render(request,"customer/success.html",{"items":items})

class OrderView(View):
    def get(self,request):
        customer = request.session.get('id')
        orders = Order.objects.filter(orderedBy=customer)
        print(orders)
        return render(request,"customer/order.html",{"orders":orders})
