from django.urls import path
from .views import Home_page


app_name = 'pages'

urlpatterns = [
    path('' , Home_page.as_view() , name='home_page'),
    # path('category/', HomePageView.as_view(), name='category'),
]