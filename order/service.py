import requests
from django.conf import settings
from django.template.loader import render_to_string
from decimal import Decimal
from django.core.mail import send_mail
from django.urls import reverse

from order.models import Order

BANK_LOGIN = settings.BANK_LOGIN
BANK_PASSWORD = settings.BANK_PASSWORD
BANK_URL = settings.BANK_URL
EMAIL_ADMIN = settings.EMAIL_HOST_USER

CURRENCY_ISO_CODES = {
    'EUR': '978',
    'USD': '840',
    'RUB': '643',
    'AMD': '051'
}


def create_payments(order_id, currency_code, request):
    """ send request to the bank for initial the payment process """
    process_url = BANK_URL + str('/register.do')

    data = {
        "orderNumber": order_id,
        "userName": BANK_LOGIN,
        "password": BANK_PASSWORD,
        "language": Order.objects.get(id=order_id).language_code,
        # "currency": CURRENCY_ISO_CODES[currency_code],
        "amount": Decimal(Order.objects.get(id=order_id).all_total * 100),
        "returnUrl": request.build_absolute_uri(reverse('order_more'))

    }

    data = requests.post(process_url, data=data).json()

    if data.get('formUrl') is not None:
        request.session['pay_order'] = order_id
        order = Order.objects.get(id=order_id)
        order.bank_order_id = data['orderId']
        order.save()
        return True, data.get('formUrl')

    return False, data


def get_order_state(order_id):
    process_url = BANK_URL + '/getOrderStatusExtended.do'
    data = {
        "orderNumber": order_id,
        "userName": BANK_LOGIN,
        "password": BANK_PASSWORD,
        "orderId": Order.objects.get(id=order_id).bank_order_id
    }
    data = requests.post(process_url, data=data).json()

    return data


def send_customers_invoice(data, request):
    message = render_to_string('email/thanks.html', {"order": data}, request=request)
    email_data = {
        "subject": "New order",
        "message": message,
        "from_email": EMAIL_ADMIN,
        "recipient_list": [data.email],
        "html_message": message,
        "fail_silently": True,

    }
    send_mail(**email_data)


def send_admins_invoice(data, request):
    message = render_to_string('email/new_order.html', {"order": data}, request=request)
    email_data = {
        "subject": "New order",
        "message": message,
        "from_email": EMAIL_ADMIN,
        "recipient_list": [EMAIL_ADMIN],
        "html_message": message,
        "fail_silently": True,

    }
    send_mail(**email_data)


def refund_price(order_id):
    process_url = BANK_URL + '/refund.do'
    data = {
        "userName": BANK_LOGIN,
        "password": BANK_PASSWORD,
        "orderId": Order.objects.get(id=order_id).bank_order_id,
        "amount": Decimal(Order.objects.get(id=order_id).all_total * 100),
    }
    data = requests.post(process_url, data=data).json()

    return True if int(data.get('errorCode')) == 0 else False
