from django.urls import path


from .views import ProductListView, ProductDetailView ,AllProductListView  , ajax_search_prodct

urlpatterns = [
    # path('search/' , search_product , name='search_product'),
    path('ajax/search/' , ajax_search_prodct , name='ajax_search_product'),
    path('' , AllProductListView.as_view(), name='all-product-list'),

    path('<slug:slug>/' , ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),



]