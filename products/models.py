from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):

    PRODUCT_OFFER = [
        ('0', ('0 %')),
        ('5', ('5 %')),
        ('10', ('10 %')),
        ('20', ('20 %')),
        ('30', ('30 %')),
        ('40', ('40 %')),
        ('50', ('50 %')),
    ]



    title = models.CharField(max_length=100 , verbose_name=_('Title'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    description = RichTextField(verbose_name=_('Description') , blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    image = models.ImageField(upload_to='products/product_cover', blank=True, null=True, verbose_name=_('Image'))
    sell_price = models.PositiveIntegerField(default=0 , verbose_name=_('Sell Price'))
    off_price = models.PositiveIntegerField(default=0 , verbose_name=_('Off Price'))
    offer = models.CharField(choices=PRODUCT_OFFER, max_length=100, verbose_name=_('Offer'))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title} - {self.is_active}'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.slug = self.slug.replace('-', ' ')
        super(Product , self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.pk])

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')