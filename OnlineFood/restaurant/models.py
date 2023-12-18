from django.db import models

class Restaurant(models.Model):
    res_name = models.CharField(max_length=50)
    min_order = models.CharField(max_length=10)
    location = models.CharField(max_length=50)

    RESTAURANT_OPEN = "Open"
    RESTAURANT_CLOSE = "Closed"
    RESTAURANT_CHOICES = (
        ('RESTAURANT_OPEN','RESTAURANT_OPEN'),
        ('RESTAURANT_CLOSE','RESTAURANT_CLOSE')
    )

    status = models.CharField(max_length=30,choices=RESTAURANT_CHOICES,default=RESTAURANT_OPEN)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return self.res_name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural= 'Categories'


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    image = models.ImageField(upload_to='food_images/')

    def __str__(self):
        return self.name

