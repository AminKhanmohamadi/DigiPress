from django import forms
from .models import Product
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'brand', 'category', 'sub_category', 'image', 'sell_price', 'off_price', 'is_active', 'offer']