from django.contrib import messages
from django.shortcuts import render, redirect

from breadcrumbs.models import BreadcrumbTexts
from .email import SendMailThread
from .forms import ContactUsRequestForm
from .models import ContactUsPage


def contact_us(request):
    form = ContactUsRequestForm(request.POST or None)
    st_content: BreadcrumbTexts = BreadcrumbTexts.objects.filter(location='contacts').first()
    contactuspage: ContactUsPage = ContactUsPage.objects.first()
    if request.method == 'POST':
        if form.is_valid():
            form = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your message has been successfully sent.<br>Our manager will contact you soon.')

            data = {
                'action': 'contact',
                'request': request,
                'first_name': form.first_name,
                'phone1': form.phone,
                'email': form.email,
                'message': form.message,
            }
            SendMailThread(data).start()
        else:
            messages.add_message(request, messages.ERROR, 'Something went wrong, please try again')
        return redirect('contact_us')

    return render(request, 'flatpages/contact_us.html', {'st_content': st_content, 'contactuspage': contactuspage})
