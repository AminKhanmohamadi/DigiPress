# Generated by Django 5.1 on 2024-09-04 09:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/product_cover', verbose_name='Image')),
                ('sell_price', models.PositiveIntegerField(default=0, verbose_name='Sell Price')),
                ('off_price', models.PositiveIntegerField(default=0, verbose_name='Off Price')),
                ('offer', models.CharField(choices=[('0', '0 %'), ('5', '5 %'), ('10', '10 %'), ('20', '20 %'), ('30', '30 %'), ('40', '40 %'), ('50', '50 %')], max_length=100, verbose_name='Offer')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
