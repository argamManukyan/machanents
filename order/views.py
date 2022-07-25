import json
import uuid

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.db import transaction

from django.template.defaultfilters import floatformat
from currencies.templatetags.currency import calculate
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.views.decorators.cache import never_cache

from cart.models import Cart
from order.models import Order, Countries, OrderStatus, Regions, OrderItem, Delivery, PaymentTypes, ProductRequest, \
    ProductRequestItem
from .forms import OrderForm
from .service import create_payments, get_order_state, send_customers_invoice, send_admins_invoice


def product_request(request, session_key):

    order = get_object_or_404(ProductRequest, session_key=session_key)

    if not order.expired_order:
        order.is_expired = True
        order.save()
        raise Http404
    items = ProductRequestItem.objects.filter(request_id=order.id)
    context = {
        'order': order,
        'is_request': True,
        'items': items,
        'request': request
    }
    if order.is_exists:
        return render(request, 'email/order_request_answer.html', context)
    return render(request, 'order/order_more.html', context)


class CheckoutView(View):
    """ atomic transaction view """

    def post(self, request, *args, **kwargs):
        LC = self.request.LANGUAGE_CODE

        region_id = request.POST.get('city_name')
        country_id = request.POST.get('country_name')
        delivery_id = request.POST.get('delivery')
        payments_id = request.POST.get('payments')

        region = None
        country = None
        if region_id and region_id.isdigit():
            region = Regions.objects.filter(id=region_id).first()

        if country_id:
            country = Countries.objects.filter(id=country_id).first()

        if request.session.get('cart_two_id'):
            cart = Cart.objects.get(id=request.session.get('cart_two_id'))
        else:
            cart = Cart.objects.get(id=request.session.get('cart_id'))

        is_request = request.POST.get('send_request')
        del_price = request.session[request.session.session_key]

        if delivery_id and int(delivery_id) == 1:
            del_price = 0
            country = None
            region = None

        if delivery_id and not Delivery.objects.filter(id=delivery_id).exists():
            return redirect('checkout')

        if payments_id and not PaymentTypes.objects.filter(id=payments_id).exists():
            return redirect('checkout')

        my_request = None
        if is_request:
            my_request = ProductRequest.objects.create(
                user_id=request.user.id or None,
                session_key=uuid.uuid4(),
                first_name=request.POST.get('first_name'),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                zip_code=request.POST.get('phone',  ''),
                country_name=country.name if country else '',
                city_name=region.name if region else '',
                delivery_price=del_price,
                address=request.POST.get('address', ''),
                notes=request.POST.get('notes', ''),
                total_price=cart.cart_total,
                all_total=cart.cart_total + del_price,
                payments_id=payments_id,
                delivery_id=delivery_id,
                curr_code=request.session.get('currency', 'AMD')
            )

            for item in cart.item.all():
                item.uuid_field = uuid.uuid4()

                item.save(force_update=True, update_fields=['uuid_field'])

                ProductRequestItem.objects.create(
                    request=my_request,
                    product_id=item.product_id,
                    product_price=item.item_price,
                    product_image=item.product.main_photo,
                    item_total_price=item.item_total_price,
                    qty=item.quantity,
                    product_name=item.product.title,
                    product_code=item.product.product_code,
                    features=item.features,
                    uuid_field=item.uuid_field
                )
        if 'send_request' in request.session:
            del request.session['send_request']

        form = OrderForm(request.POST)

        if form.is_valid():
            order: Order = form.save(commit=False)
            if request.user:
                order.user_id = request.user.id

            order.total_price = cart.cart_total
            order.payments_id = payments_id
            order.language_code = LC
            order.hidden = is_request is None
            order.request_id = my_request.id if my_request else None
            order.delivery_id = delivery_id
            order.country_name = country.name if country else ''
            order.city_name = region.name if region else ''
            order.order_status_id = OrderStatus.objects.order_by('-id')[1].id
            order.curr_code = request.session['currency']
            order.session_key = request.session.session_key or request.session.cycle_key()
            order.delivery_price = del_price
            order.all_total = order.total_price + order.delivery_price
            order.save()

            for item in cart.item.all():
                OrderItem.objects.create(
                    order_id=order.id,
                    product=item.product,
                    product_name=item.product.title,
                    product_image=item.product.main_photo,
                    product_price=item.item_total_price / item.quantity,
                    qty=item.quantity,
                    item_total_price=item.item_total_price,
                    description=item.features,
                    uuid_field=item.uuid_field
                )
                item.delete()

            cart.delete()

            if payments_id and int(payments_id) == 2:
                pass
                # status, data = create_payments(order.id, order.curr_code, request)
                # if status:
                #     send_customers_invoice(order, request)
                #     send_admins_invoice(order, request)
                #     return HttpResponseRedirect(data)
                # else:
                #     if OrderStatus.objects.filter(id=3).exists():
                #         pass
                #         # order.order_status_id = 3
                #     else:
                #         order.order_status = None
                #     order.save()
                #     # return redirect('checkout')
                #     return JsonResponse(data=data, safe=False)
            if not my_request:
                messages.success(request, _('Պատվերը հաջողությամբ ձևակերպվել է։'))
                return redirect('order_more')
            else:
                request.session['is_req'] = True
                messages.success(request, _('Հարցումը հաջողությամբ ուղարկվել է։'))
                return redirect(reverse('product_request', kwargs={'session_key': my_request.session_key}))

        return redirect('checkout')

    @never_cache
    def get(self, request, **kwargs):

        try:
            if request.session.get('cart_two_id'):
                cart = Cart.objects.get(id=request.session.get('cart_two_id'))
            else:
                cart = Cart.objects.get(id=request.session.get('cart_id'))
        except Cart.DoesNotExist:
            return redirect('home')
        if not cart or cart.cart_total == 0:
            return redirect('home')
            # delivery_times = DeliveryTime.objects.all()
            # states = State.objects.order_by('id')
            #
            # del_price = 0
            # if request.user.is_authenticated and request.user.profile.city_id:
            #     del_price = request.user.profile.city.price
            #
        delivery_types = Delivery.objects.order_by('-id')

        sumItemsTotal = 0
        countries = Countries.objects.order_by('name')
        regions = Regions.objects.order_by('name')

        kilo_summary = 0

        for i in cart.item.all():
            kilo_summary += i.quantity * float(i.product.weight)
            sumItemsTotal += i.item_total_price

        if request.is_ajax():

            del_up = False
            if request.GET.get('region_id') and request.GET.get('region_id').isdigit():
                current_region = Regions.objects.get(id=int(request.GET.get('region_id')))
                if current_region.del_up:
                    del_up = True
            elif (request.GET.get('region_id') != [''] and not request.GET.get('country_id')):
                request.session[request.session.session_key] = 0
                return JsonResponse({'delivery_price': 0}, safe=False)

            if request.GET.get('country_id'):
                country_id = request.GET.get('country_id')
            else:
                country_id = str(current_region.country.id)

            if not country_id.isdigit():
                request.session[request.session.session_key] = 0
                return JsonResponse({'delivery_price': 0})
            current_country = Countries.objects.get(id=int(country_id))
            """Այս դեպքում երկիրը ունի ֆիքս արժեքներ և չունի զոնա 
                //////////////////////////////////////
               Առաջին պայմանով ստուգում ենք արդյոք մեր զամբյուղի առկա ապրանքնրի քաշերի գումարը տվյալ երկրի 
               մինիմալ արժեքից (Եթե կա այն ) փոքքր է թե ոչ:
               Երկրորդ պայմանով ստուգում ենք թե մեր զամբյուղի քաշը գտնվում է արդյոք տվյալ երկրի քաշային ռենջի մեջ։
               Երրորդ պայմանով ստուգում ենք այն դեպքը երբ տվյալ զամբյուղի քաշը մեծ է երկրների առավելագույն ֆիքս․ քաշից 
               ու այդ պայմանից ելնելով հաշվարկում ենք գումարը
               ////////////////////////////////////////// 
            """
            try:
                if request.GET.get('region_id') and request.GET.get('region_id').isdigit():
                    current_region = Regions.objects.get(id=int(request.GET.get('region_id')))

                if current_country.regions_set.count():
                    if not request.GET.get('region_id') and not current_country.regions_set.count():
                        request.session[request.session.session_key] = 0
                        return JsonResponse({'delivery_price': 0}, safe=False)
                    for fix_kilo in current_country.fixedvalues_set.all():
                        if kilo_summary > 20 and del_up:
                            request.session[request.session.session_key] = current_country.fixedvalues_set.last().fixed_price
                            return JsonResponse({'delivery_price': calculate(
                                current_country.fixedvalues_set.last().fixed_price, request.session['currency'])})
                        if kilo_summary > 20 and del_up is False:
                            return JsonResponse({'delivery_price': 'dont_delivery'})

                        if fix_kilo.fixed_gramm > kilo_summary:
                            request.session[request.session.session_key] = fix_kilo.fixed_price
                            return JsonResponse(
                                {'delivery_price': calculate(fix_kilo.fixed_price, request.session['currency'])})
                            break
                    request.session[request.session.session_key] = 0
                    return JsonResponse({'delivery_price': 0})

                if current_country.fixedvalues_set.count() and current_country.zonas == None:

                    if current_country.regions_set.count():
                        request.session[request.session.session_key] = 0
                        return JsonResponse({'delivery_price': 0})
                    if current_country.round_maark and kilo_summary > 0 and kilo_summary < current_country.round_maark:
                        request.session[request.session.session_key] =  current_country.fixedvalues_set.first().fixed_price
                        return JsonResponse({'delivery_price': calculate(
                            current_country.fixedvalues_set.first().fixed_price, request.session['currency'])})
                    if float(kilo_summary) >= float(current_country.fixedvalues_set.first().fixed_gramm) and float(
                            kilo_summary) <= float(current_country.fixedvalues_set.last().fixed_gramm):

                        if current_country.round_maark:
                            fixing_gramms = float("{:.2f}".format(kilo_summary % current_country.round_maark))
                        else:
                            fixing_gramms = float("{:.2f}".format(kilo_summary))

                        if fixing_gramms > 0.0:
                            computed_kilo = kilo_summary + float(
                                current_country.round_maark - float("{:.2f}".format(fixing_gramms)))

                            getv = 0
                            for fix_kilo in current_country.fixedvalues_set.all():
                                if fix_kilo.fixed_gramm >= computed_kilo:
                                    getv = fix_kilo.fixed_price
                                    break

                            request.session[request.session.session_key] = float('{:.0f}'.format(getv))

                            return JsonResponse({'delivery_price': float('{:.0f}'.format(getv))})
                            # test
                        else:
                            computed_kilo = kilo_summary
                            for fix_kilo in current_country.fixedvalues_set.all():
                                if fix_kilo.fixed_gramm == computed_kilo:
                                    request.session[request.session.session_key] = float('{:.0f}'.format(fix_kilo.fixed_price,))
                                    return JsonResponse({'delivery_price': float(
                                        '{:.0f}'.format(calculate(fix_kilo.fixed_price, request.session['currency'])))})
                    else:

                        if not current_country.round_maark and current_country.fixes_price:
                            computed_price = current_country.fixes_price + current_country.every_rounded_price * kilo_summary
                            request.session[request.session.session_key] = float('{:.0f}'.format(computed_price))
                            return JsonResponse({'delivery_price': float(
                                '{:.0f}'.format(calculate(computed_price, request.session['currency'])))})

                        if current_country.round_maark:
                            fixing_gramms = float(kilo_summary % current_country.round_maark)
                        else:
                            fixing_gramms = float(kilo_summary)

                        if fixing_gramms > 0.0:

                            computed_kilo = kilo_summary + float(
                                current_country.round_maark - float("{:.2f}".format(fixing_gramms)))
                        else:
                            computed_kilo = kilo_summary

                        if current_country.fixes_price:

                            computed_price = current_country.fixes_price + float(computed_kilo / float(
                                "{:.2f}".format(current_country.round_maark))) * current_country.every_rounded_price
                        else:
                            # print(current_country.fixedvalues_set.first().fixed_price,computed_kilo)
                            computed_price = current_country.fixedvalues_set.first().fixed_price + float((
                                                                                                                 computed_kilo / float(
                                                                                                             "{:.2f}".format(
                                                                                                                 current_country.round_maark))) - current_country.fixedvalues_set.first().fixed_gramm) * current_country.every_rounded_price
                            request.session[request.session.session_key] = float('{:.0f}'.format(computed_price))
                        return JsonResponse({'delivery_price': float(
                            '{:.0f}'.format(calculate(computed_price, request.session['currency'])))})

                        """Այս դեպքում երկիրը ունի ֆիքս արժեքներ և չունի զոնա"""
                else:
                    zona_fixed_price = current_country.zonas.fixed_price
                    zona_roundable_kilo = current_country.zonas.round_maark
                    zona_roundable_price = current_country.zonas.every_rounded_price

                    if kilo_summary <= zona_roundable_kilo:
                        request.session[request.session.session_key] = float('{:.0f}'.format(zona_fixed_price))
                        return JsonResponse({'delivery_price': float(
                            '{:.0f}'.format(calculate(zona_fixed_price, request.session['currency'])))})
                    else:

                        fixed_kilo = kilo_summary % zona_roundable_kilo

                        if fixed_kilo == 0.0:
                            computed_kilo = kilo_summary
                        else:
                            computed_kilo = kilo_summary + float(zona_roundable_kilo - fixed_kilo)

                        computed_price = float(zona_fixed_price) + float(
                            (computed_kilo - zona_roundable_kilo) * zona_roundable_price)
                        request.session[request.session.session_key] = float(
                            '{:.0f}'.format(computed_price))
                        return JsonResponse({'delivery_price': float(
                            '{:.0f}'.format(calculate(computed_price, request.session['currency'])))})

            except ObjectDoesNotExist:
                request.session[request.session.session_key] = 0
                return JsonResponse(
                    {'delivery_price': float('{:.0f}'.format(calculate(0, request.session['currency'])))})
        return render(request, 'order/checkout.html',
                      {'countries': countries,
                       'regions': regions,
                       'cart': cart,
                       'delivery_types': delivery_types})


class OrderMoreView(View):

    @never_cache
    def get(self, request, **kwargs):
        try:
            order = Order.objects.filter(session_key=request.session.session_key).order_by('-id').first()
        except Exception as e:
            return redirect('home')

        if 'orderId' in request.GET:
            data = get_order_state(order.id, request)
            order.bank_order_status = int(data['orderStatus'])
            if int(data['orderStatus']) == 2:
                order.bank_message = "Պատվերը հաջողությամբ ձևակերպվել է"
                order.order_status = OrderStatus.objects.filter(title_hy='Վճարված').first()
                order.is_paid = True
            else:
                order.bank_message = "Տեղի է ունեցել սխալ"
                order.order_status = OrderStatus.objects.filter(title_hy='Չվճարված').first()
            order.save()
            send_customers_invoice(order, request)
            send_admins_invoice(order, request)
            return HttpResponseRedirect(reverse('order_more'))

        if not order:
            return redirect('home')
        items = OrderItem.objects.filter(order_id=order.id)
        return render(request, 'order/order_more.html', {'order': order, 'items': items})


class BuyNowView(View):

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        product_id = data.pop('product_id')
        quantity = data.pop('quantity')

        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_two_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        request.session['cart_two_items'] = cart.item.count()

        if cart.item.filter(product_id=product_id, features__contains=data).exists():
            item = cart.item.filter(product_id=product_id, features__contains=data).first()
            item.quantity += int(quantity)
            item.save()
        else:
            cart.item.create(product_id=product_id, features=data, quantity=quantity)
        cart_total = 0
        for i in cart.item.all():
            cart_total += i.item_total_price
        cart.cart_total = cart_total
        cart.save()

        language_code = '' if request.LANGUAGE_CODE == settings.LANGUAGE_CODE else f'/{request.LANGUAGE_CODE}'

        url = f'http://{request.get_host()}' + reverse('checkout')

        return JsonResponse({'cart_items': cart.item.count(), 'redirect_url': url}, status=200)


def send_request(request):
    data = json.loads(request.body)
    product_id = data.pop('product_id')

    cart = Cart()
    cart.save()
    cart_id = cart.id
    request.session['cart_two_id'] = cart_id
    cart = Cart.objects.get(id=cart_id)
    request.session['cart_two_items'] = cart.item.count()
    print(data)

    item = cart.item.create(product_id=product_id, features=data, quantity=1)
    print(item.features)
    cart_total = sum(i.item_total_price for i in cart.item.all())
    cart.cart_total = cart_total
    cart.save()

    language_code = '' if request.LANGUAGE_CODE == settings.LANGUAGE_CODE else f'/{request.LANGUAGE_CODE}'

    url = f'http://{request.get_host()}' + reverse('checkout')
    request.session['send_request'] = True
    return JsonResponse({'cart_items': cart.item.count(), 'redirect_url': url}, status=200)
