from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from products.models import Product


# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey(get_user_model() , on_delete=models.CASCADE , verbose_name=_('User'))
    product = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_('Product'))
    datetime_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'product'),)
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')

    def __str__(self):
        return f"{self.user} - {self.product.title}"
