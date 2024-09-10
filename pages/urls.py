from django.urls import path
from .views import Home_page , favorite_list_view , add_to_favorite_view ,remove_favorite_view


app_name = 'pages'

urlpatterns = [
    path('' , Home_page.as_view() , name='home_page'),
    # path('category/', HomePageView.as_view(), name='category'),
    path('favorites/', favorite_list_view, name='favorite_products'),
    path('favorites/add/<int:product_id>/', add_to_favorite_view, name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', remove_favorite_view, name='remove_from_favorites'),


]