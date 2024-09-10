from django.shortcuts import render

# Create your views here.
def order_create(request):
    return render(request, 'orders/order_create.html')