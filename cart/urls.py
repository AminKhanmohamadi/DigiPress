from django.urls import path

from .views import *

urlpatterns = [
    path('' , cart_detail_view , name='cart_detail'),
    path('add/<int:product_id>/' , add_to_cart_view , name='add_to_cart'),
    path('remove/<int:product_id>/' , remove_from_cart_view , name='remove_from_cart'),
]