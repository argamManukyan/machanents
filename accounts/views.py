from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.views import View
from django.views.generic import DetailView
from django.utils.translation import ugettext_lazy as _
from order.models import Order, Countries, Regions, ProductRequest
from .forms import CustomUserForm, UpdateProfile
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import SendMail
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from datetime import datetime


class RegisterView(View):

    def post(self, request, **kwargs):

        form = CustomUserForm(request.POST)

        if User.objects.filter(email=request.POST.get('email')).exists():
            messages.error(request, _('Նշված էլ. փոստի հասցե ունեցող օգտատեր արդեն գոյություն ունի։'))
            return redirect('register')
        message_type = None
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.email.split('@')[0] + str(datetime.now().microsecond)
            new_user.is_active = False
            new_user.save()
            messages.success(request,
                             _('Շնորհակալություն գրանցման համար:<br/> Խնդրում ենք հաստատեք Ձեր էլ. փոստի հասցեն '
                               'գրանցումն ավարտելու համար:'))
            data = {'user': new_user, 'request': request}
            SendMail.send_activation_message(data)
            return redirect('login')
        else:
            messages.error(request, _('Տեղի է ունեցել սխալ։ Խնդրում ենք կրկին փորձել։'))
            return redirect('register')

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'accounts/sign_up.html')


class ActivationEmail(View):

    def get(self, request, **kwargs):

        if request.user.is_authenticated:
            return redirect('profile')

        try:
            _kw_uid = kwargs.get('uid64')
            _kw_token = kwargs.get('token')
            user_id = force_text(urlsafe_base64_decode(_kw_uid))
            user = User.objects.get(id=user_id)

            if user.is_active:
                return HttpResponse(_('Հղումն արդեն օգտագործվել է:'))

            if PasswordResetTokenGenerator().check_token(user=user, token=_kw_token):
                user.is_active = True
                user.save(force_update=True)
                Profile.objects.create(user_id=user.id)
            else:
                user.delete()
                return HttpResponse(_('Տեղի է ունեցել սխալ։ Խնդրում ենք նորից գրանցվել։'))


        except User.DoesNotExist:
            return HttpResponse(_("Օգտատերը չի գտնվել։"))

        messages.success(request, _('Շնորհակալություն, Ձեր էջը հաջղությամբ ակտիվացված է:'))

        return redirect('login')


class LoginView(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'accounts/sign_in.html')

    def post(self, request, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember' or None)

        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Նշված էլ. փոստի հասցե ունեցող օգտատեր չի գտնվել։')
            return redirect('login')

        if User.objects.filter(email=email, is_active=False).exists():
            messages.error(request, 'Հաստատեք Ձեր էլ. փոստի հասցեն, որպեսզի կարողանաք շարունակել։')
            return redirect('login')

        check_user = User.objects.get(email=email)

        if user := authenticate(username=check_user.username, password=password):
            login(request, user)

            if not remember:
                self.request.session.set_expiry(0)

            return redirect('home')
        else:
            messages.error(request, 'Սխալ մուտքանուն կամ գաղտնաբառ։')
            return redirect('login')


class ForgotPassword(View):

    def post(self, request, **kwargs):

        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(request, _('Նշված էլ. փոստի հասցե ունեցող օգտատեր չի գտնվել։'))
            return redirect(request.get_full_path())

        data = {'user': User.objects.get(email=email), 'request': request}
        SendMail.send_password_reset_mail(data)
        messages.success(request, _(f"Գաղտնաբառի փոփոխման նամակը ուղարկվել է {email} էլ. փոստի հասցեին։"))

        return redirect('login')

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, 'accounts/forgot_password.html')


class NewPasswordView(View):

    def get(self, request, **kwargs):

        try:
            user_id = urlsafe_base64_decode(kwargs.get('uid64'))
            token = kwargs.get('token')
            user = User.objects.get(id=user_id)
            user_token = PasswordResetTokenGenerator().check_token(user=user, token=token)
        except:
            messages.error(request, _('Տեղի է ունեցել սխալ։ Խնդրում ենք կրկին փորձել։'))
            return redirect('forgot')

        return render(request, 'accounts/new_password.html')

    def post(self, request, **kwargs):

        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password2')

        if pass2 != pass1:
            messages.error(request, _('Գաղտնաբառը չի համընկնում։'))
            return redirect('password_reset_confirm')

        user_id = urlsafe_base64_decode(kwargs.get('uid64'))
        user = User.objects.get(id=user_id)

        user.set_password(pass1)
        user.save()
        messages.success(request, _('Ձեր գաղտնաբառը հաջողությամբ վերականգնվել է։'))
        return redirect('login')


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        user: User = request.user
        if not user.profile:
            Profile.objects.create(user_id=user.id)
        profile = Profile.objects.get(user_id=user.id)
        orders = Order.objects.filter(user_id=user.id, bank_order_status__isnull=False,
                                      request_id__isnull=False)
        requests_list = ProductRequest.objects.filter(is_expired=False)
        product_requests = ProductRequest.objects.all()
        countries = Countries.objects.order_by('name')
        regions = Regions.objects.all().order_by('name')
        request_list = ProductRequest.objects.filter(is_exists=False)

        context = {
            'profile': profile,
            'orders': orders,
            'requests_list': requests_list,
            'product_requests': product_requests,
            'countries': countries,
            'request_list': request_list,
            'regions': regions,
            'user': user
        }

        return render(request, 'accounts/profile_page.html', context)

    def post(self, request, **kwargs):
        form = UpdateProfile(request.POST, instance=request.user.profile)
        country = request.POST.get('country', None)
        region = request.POST.get('region', None)
        first_name = request.POST.get('first_name', None)

        if country and int(country) != 1:
            region = None

        if form.is_valid():
            profile = form.save(commit=False)
            if country:
                profile.country_id = country
            else:
                profile.country = None
            if region:
                profile.region_id = region
            else:
                profile.region = None

            if first_name:
                profile.user.first_name = first_name
                profile.user.save()
            profile.save()
            messages.success(request, _('Ձեր տվյալները հաջողությամբ թարմացվել են։'))
            return redirect('profile')
        else:

            messages.error(request, _('Տեղի է ունեցել սխալ։ Խնդրում ենք կրկին փորձել։'))
            return redirect('profile')


class ChangePasswordView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):

        old_password = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')

        if confirmpassword != newpassword:
            messages.error(request, _('Գաղտնաբառը չի համընկնում։'))
            return redirect('profile')

        if request.user.check_password(old_password):

            request.user.set_password(newpassword)
            request.user.save()
            login(request, request.user)
            messages.success(request, _('Ձեր գաղտնաբառը հաջողությամբ թարմացվել է։'))
            return redirect('profile')

        else:
            messages.error(request, _('Ձեր հին գաղտնաբառը սխալ է մուտքագրված։ Խնդրում նեք մուտքագրել նորից։'))
            return redirect('profile')


def logout_view(request):
    logout(request)
    return redirect('home')


class OrderDetails(LoginRequiredMixin, DetailView):
    template_name = 'order/order_more.html'
    model = Order
    context_object_name = 'order'
    slug_field = 'pk'

    def get_queryset(self):
        qs = Order.objects.filter(user_id=self.request.user.id)
        return qs

    def get(self, request, *args, **kwargs):
        if not Order.objects.filter(user_id=request.user.id, id=kwargs.get('pk')).exists():
            return redirect('profile')
        return super().get(request, *args, **kwargs)
