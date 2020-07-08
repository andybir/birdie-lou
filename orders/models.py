from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from coupons.models import Coupon
from django_countries.fields import CountryField

class Order(models.Model):
    first_name = models.CharField('first name', 
                                  max_length=50)
    last_name = models.CharField('last name', 
                                 max_length=50)
    email = models.EmailField('e-mail',)
    address = models.CharField('address', 
                               max_length=250)
    city = models.CharField('city', 
                            max_length=100)
    country = CountryField(blank_label='United States',
                           default=False)
    state = models.CharField('state',
                             max_length=100,
                            default=False)
    postal_code = models.CharField('postal code', 
                                   max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all()) 
        return total_cost - total_cost * \
            (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity