from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem
from django.utils.translation import gettext as _

# Create your views here.

@login_required
def order_create(request):
    cart = Cart(request)
    order_form = OrderForm()

    if len(cart) == 0:
        messages.warning(request, _('No orders available'))
        return redirect('all-product-list')


    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price = product.get_price(),
                )
                cart.clear()
                request.user.first_name = order_obj.first_name
                request.user.last_name = order_obj.last_name
                request.user.phone_number = order_obj.phone_number
                request.user.address = order_obj.address
                request.user.postal_code = order_obj.postal_code
                request.user.save()

                request.session['order_id'] = order_obj.id
                return redirect('payment:payment_process')


    return render(request, 'orders/order_create.html' , {'form': order_form})


