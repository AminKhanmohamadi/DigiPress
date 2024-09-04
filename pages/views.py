from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class Home_page(View):
    def get(self, request):
        return render(request , 'pages/home_page.html')
