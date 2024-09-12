from pydoc import resolve

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100 , verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100 , verbose_name=_('Last Name'))

    phone_number = models.CharField(max_length=15 , verbose_name=_('Phone Number'))
    address = models.CharField(max_length=700 , verbose_name=_('Address'))
    postal_code = models.CharField(max_length=100 , verbose_name=_('Postal Code'))

    authority = models.CharField(max_length=255 , verbose_name=_('Authority') , blank=True)
    ref_id = models.CharField(max_length=255 , verbose_name=_('Ref_id') , blank=True)
    zarinpal_data = models.TextField(blank=True)

    is_paid = models.BooleanField(default=False)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.user}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


    def get_total_price(self):
        result = 0
        # for item in self.items.all():
        #     result += item.price * item.quantity
        # return result
        return sum(item.quantity * item.price for item in self.items.all())




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='order_items')
    quantity = models.PositiveIntegerField(default=1 , verbose_name=_('Quantity'))
    price = models.DecimalField(max_digits=10, decimal_places=0 , verbose_name=_('Price'))

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} * {self.quantity} = {self.price}'

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def final_price(self):
        if Product.sell_price:
            return Product.sell_price == self.price
        else:
            return Product.off_price == self.price








