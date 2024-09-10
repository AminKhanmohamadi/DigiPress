from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    slug = models.SlugField(max_length=100, verbose_name=_('Slug'), blank=True, null=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_clean_slug(self):
        return self.slug.replace('-', ' ')


class SubCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    slug = models.SlugField(max_length=100, verbose_name=_('Slug'), blank=True, null=True, unique=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('Category'))
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='sub_category', verbose_name=_('Sub Category'))
    brand = models.CharField(max_length=100, verbose_name=_('Brand'), null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    description = RichTextField(verbose_name=_('Description'), blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    image = models.ImageField(upload_to='products/product_cover', blank=True, null=True, verbose_name=_('Image'))
    sell_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_('Sell Price'))
    off_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_('Off Price'), null=True, blank=True)
    offer = models.PositiveIntegerField(verbose_name=_('Offer'), null=True, blank=True,
                                        validators=[MinValueValidator(1), MaxValueValidator(100)])

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.is_active}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.offer and self.offer > 0:
            sell_price = Decimal(self.sell_price)
            offer = Decimal(self.offer)
            discount = (offer / Decimal('100')) * sell_price
            self.off_price = sell_price - discount
        super().save(*args, **kwargs)

    def get_clean_slug(self):
        return self.slug.replace('-', ' ')

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])

    def get_price(self):
        return self.off_price if self.offer else self.sell_price

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
