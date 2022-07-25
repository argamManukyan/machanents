from django.core.mail import send_mail
from threading import Thread
from django.conf import settings
from django.template.loader import render_to_string

ADMIN_EMAIL = settings.EMAIL_HOST_USER

class SendMailThread(Thread):

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self) -> None:
        data = self.data
        if self.data['action'] == 'contact':
            message = render_to_string('email/contact_request.html', data, data['request'])
            send_mail("Հետադարձ կապի պատվեր", message=message, from_email=ADMIN_EMAIL,
                      recipient_list=[ADMIN_EMAIL], html_message=message, fail_silently=True)
        else:
            message = render_to_string('email/new_booking.html', data, data['request'])
            send_mail("Խորհրդատվության պատվեր", message=message, from_email=ADMIN_EMAIL,
                      recipient_list=[ADMIN_EMAIL], html_message=message, fail_silently=True)
