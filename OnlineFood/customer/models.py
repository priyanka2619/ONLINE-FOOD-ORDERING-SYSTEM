from django.db import models
from restaurant.models import MenuItem,Restaurant


class Customer(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    phone = models.IntegerField(unique=True)
    address = models.TextField()
    image = models.ImageField(upload_to='customer_images/')

    def __str__(self):
        return self.email


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    orderedBy = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    m_no = models.CharField(max_length=20)

    price = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    biling_name = models.CharField(max_length=50,default=0)
    biling_mno = models.IntegerField(default=0)
    biling_address = models.CharField(max_length=60, blank=True,default=0)
    shipping_name = models.CharField(max_length=50,default=0)
    shipping_mno = models.IntegerField(default=0)
    shipping_address = models.CharField(max_length=60, blank=True,default=0)


    ORDER_WAITING = 'Waiting'
    ORDER_PLACED = 'Placed'
    ORDER_ACCEPTED = 'Accepted'
    ORDER_COMPLETED = 'Completed'
    ORDER_CANCELLED = 'Cancelled'
    ORDER_DISPATCHED = 'Dispatched'

    ORDER_CHOICES = (
        ('ORDER_WAITING','ORDER_WAITING'),
        ('ORDER_PLACED','ORDER_PLACED'),
        ('ORDER_ACCEPTED','ORDER_ACCEPTED'),
        ('ORDER_COMPLETED','ORDER_COMPLETED'),
        ('ORDER_CANCELLED','ORDER_CANCELLED'),
        ('ORDER_DISPATCHED','ORDER_DISPATCHED')
    )
    status = models.CharField(max_length=50,choices=ORDER_CHOICES,default=ORDER_WAITING)

    def placeOrder(self):
        self.save()

    def __str__(self):
        return self.orderedBy.email



