from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

from django.conf import settings

admin_email = settings.EMAIL_HOST_USER


# decorator for anonymous users

# def role_required(allowed_roles=[]):
#     def decorator(view_func):
#         def wrap(request, *args, **kwargs):
#             if request.user.profile.userStatus in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return render(request, "dashboard/404.html")
#         return wrap
#     return decorator

# def anonymous_user(request):
#     def decorator(view_func):
#         def wrapper(request,*args,**kwargs):
#             if request


class SendMail:

    @staticmethod
    def send_activation_message(data):
        user = data.get('user')
        request = data.get('request')

        site = get_current_site(request).domain
        uid64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)

        url = 'http://' + site + reverse('activation', kwargs={"uid64": uid64, "token": token})
        recipient_list = [user.email]
        message = render_to_string('email/activation.html', {'user': user, 'site': site, 'link': url}, request=request)

        send_mail(_('Պրոֆիլի ակտիվացում '), message, from_email=admin_email, recipient_list=recipient_list,
                  html_message=message)

    # @staticmethod
    # def send_confirmation_message(data):
    #     request = data.get('request')
    #     recipient_list = [data.get('email')]
    #     type_of_confirm = data.get('type')

    #     site = get_current_site(request).domain
    #     message = render_to_string('email/confirmation.html',{'request':request,
    #                                                         'site':site,
    #                                                         'type':type_of_confirm})

    #     send_mail(message,from_email=admin_email,
    #                     recipient_list=recipient_list,html_message=message)

    @staticmethod
    def send_password_reset_mail(data):
        user = data.get('user')
        request = data.get('request')

        site = get_current_site(request).domain
        uid64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)
        request.session['password_reset_token'] = token

        url = 'http://' + site + '/password-reset-confirm/' + uid64 + '/' + token + '/'
        recipient_list = [user.email]
        message = render_to_string('email/password-reset.html', {'user': user, 'site': site, 'link': url},
                                   request=request)

        send_mail(_('Գաղտնաբառի վերականգնում '), message, from_email=admin_email, recipient_list=recipient_list,
                  html_message=message)
