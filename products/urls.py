from django.urls import path

from .views import ProductListView, ProductDetailView ,AllProductListView

urlpatterns = [
    path('' , AllProductListView.as_view(), name='all-product-list'),
    path('<slug:slug>/' , ProductListView.as_view(), name='product_list'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]