import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from donation.models import DonationCurrencies, Donations


def send_donation(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('contact_us'))
    data = json.loads(request.body)
    currency = DonationCurrencies.objects.filter(id=data.pop('currency_id')).first()

    if not currency:
        return HttpResponse(status=400)

    data['currency'] = currency.name
    radio = data.pop('radio', '')

    if radio == 'on':
        Donations.objects.create(**data)
    else:
        print(radio)
        Donations.objects.create(amount=data['amount'], currency=data['currency'])
    return HttpResponse(status=200)
