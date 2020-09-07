from django.db import models
from django.contrib.auth.models import User
import decimal

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Name', max_length=100, null=True)
    email = models.EmailField('Email', max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Category(models.Model):
    name = models.CharField('Name', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Company(models.Model):
    name = models.CharField('Name', max_length=20)
    country = models.CharField('Country', max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField('Name', max_length=50, null=True)
    description = models.TextField('Description', max_length=3000, blank=True, null=True)
    specifications = models.TextField('Specifications', max_length=3000, null=True)
    #price = models.FloatField('Price', default=0)
    price = models.DecimalField('Price', default=0, max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField('Discount', default=0, null=True)
    year = models.PositiveSmallIntegerField('Year', default=2020)
    digital = models.BooleanField(default=False, null=True, blank=False)
    isActive = models.BooleanField(default=True)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        return self.price * decimal.Decimal(1 - self.discount / 100)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'media/placeholder.png'
        return url

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    data_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def shipping(self):
        shipping = False;
        orderItems = self.orderitem_set.all()

        for item in orderItems:
            if item.product.digital == False:
                shipping = True
        return shipping

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.discount_price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField('Country', max_length=30, null=True)
    city = models.CharField('City', max_length=30, null=True)
    state = models.CharField('State', max_length=30, null=True)
    address = models.CharField('Address', max_length=200, null=True)
    zipcode = models.CharField('Zipcode', max_length=10, null=True)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Shipping address'
        verbose_name_plural = 'Shipping addresses'
