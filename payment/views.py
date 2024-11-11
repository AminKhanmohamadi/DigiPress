import requests
import json
from django.shortcuts import get_object_or_404 ,redirect ,reverse
from orders.models import Order
from django.conf import settings
from django.http import HttpResponse

from orders.models import Order


# Create your views here.
def payment_process(request):
    # Get order id to from session
    order_id = request.session.get('order_id')

    # Get the order object
    order = get_object_or_404(Order, pk=order_id)

    toman_total_price = int(order.get_total_price())

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'currency' : 'IRT',
        'amount' : toman_total_price,
        'description' : f'#{order.id} : {order.user.first_name} {order.user.last_name}',
        'callback_url' :request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()['data']
    print(data)
    authority = data['authority']
    order.authority = authority
    order.save()

    if  'errors' not  in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')

def payment_callback_view(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order , authority=payment_authority)

    toman_total_price = int(order.get_total_price())

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'currency': 'IRT',
            'amount': toman_total_price,
            'authority': payment_authority,
        }

        res = requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
        )



        if 'data' in res.json()  and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')

            elif payment_code == 101:
                return HttpResponse('پرداخت شما با موفقیت انجام شد.البته این تراکنش قبلا ثبت شده است.')

            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                return HttpResponse(f'تراکنش ناموفق بود{error_code} {error_message}')

    else:
        return HttpResponse('تراکنش نا موفق بود')





def payment_process_sandbox(request):
    # Get order id to from session
    order_id = request.session.get('order_id')

    # Get the order object
    order = get_object_or_404(Order, pk=order_id)

    toman_total_price = int(order.get_total_price())

    zarinpal_request_url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json'
    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    request_data = {
        'merchant_id': 'abcABCabcABCabcABCabcABCabcABCabcABC',
        'amount' : toman_total_price,
        'currency' : 'IRT',
        'description' : f'#{order.id} : {order.user.first_name} {order.user.last_name}',
        'callback_url' :request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    print(res)
    data = res.json()
    print(data)
    authority = data['authority']
    order.authority = authority
    order.save()

    if  'errors' not  in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')

def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order , authority=payment_authority)

    toman_total_price = int(order.get_total_price())

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        request_data = {
            'MerchantID': 'abcABCabcABCabcABCabcABCabcABCabcABC',
            'Currency': 'IRT',
            'Amount': toman_total_price,
            'Authority': payment_authority,
        }

        res = requests.post(
            url='https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
        )



        if 'data' in res.json()  and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')

            elif payment_code == 101:
                return HttpResponse('پرداخت شما با موفقیت انجام شد.البته این تراکنش قبلا ثبت شده است.')

            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                return HttpResponse(f'تراکنش ناموفق بود{error_code} {error_message}')

    else:
        return HttpResponse('تراکنش نا موفق بود')