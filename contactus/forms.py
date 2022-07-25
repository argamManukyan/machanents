from django import forms
from django.forms import ModelForm

from .models import *


class ContactUsRequestForm(ModelForm):
    class Meta:
        model = ContactUsRequest
        exclude = ['my_order']


class BookingsForm(ModelForm):

    class Meta:
        model = Bookings
        exclude = ['time_of_pick']
