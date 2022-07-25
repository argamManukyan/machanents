import json
import random
from django.urls import reverse
from django.db.models.aggregates import Avg, Max, Min
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View, generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import floatformat
from currencies.utils import convert
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from donation.models import DonationCurrencies, DonationRanges, DonationHomepageText
from flatpages.models import Blog, AboutUs
from videos.models import Video
from .models import Category, Color, FilterField, Product, FilterValue, ProductFeature, Rating, RatingProduct, \
    ViewedProducts, Slider, \
    OurAdvantages, SpecialOfferBanner, TermsAndConditions, PrivacyPolicy, DeliveryAndPayMent, HomepageUnderSliderText, \
    AboutUsHomePageText, Authors, AuthorCategories, ProductReviews

from breadcrumbs.models import BreadcrumbTexts


def get_ip_client(request):
    """ Method for get user ip address """

    return x_forwarded_for.split(',')[0] if (
        x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR')) else request.META.get('REMOTE_ADDR')


def get_donation_amounts(request, obj_id):

    currency_names = get_object_or_404(DonationCurrencies, id=obj_id)

    donation_currencies = list(DonationRanges.objects.filter(currency_name_id=obj_id).values_list('amount', flat=True))
    limit = round(convert(900_000, 'AMD', currency_names.name))
    return JsonResponse(
        {'donation_currencies': donation_currencies,
         'limit': limit,
         'currName': currency_names.name
         })


class HomeView(View):
    """ Home page, there is logic for shown category items, so which category will
        first in admin panel that is will shown with 8 items , others will shown with 4 items
    """

    @never_cache
    def get(self, request, **kwargs):

        second_items, three_items = None, None

        # slider
        slider_items = Slider.objects.all()
        homepage_about = AboutUsHomePageText.objects.last()
        homepage_text = HomepageUnderSliderText.objects.last()
        category_icons = Category.objects.filter(show_in_homepage=True)

        # DONATION
        reviews = ProductReviews.objects.order_by('-id')
        donation_currencies = DonationCurrencies.objects.all()
        donation_amounts = None
        if donation_currencies:
            donation_amounts = DonationRanges.objects.filter(currency_name_id__in=[donation_currencies.first().id])
        donation_homepage_content = DonationHomepageText.objects.last()

        # Donation

        machanents_videos = Video.objects.filter(show_on_homepage=True)
        # Fragment for first product shown slider
        selected_category = Category.objects.filter(parent=None)
        list_ids_cat = []
        products_for_homepage = Product.objects.filter(show_in_homepage=True)
        if selected_category:
            list_ids_cat = [index.id for index in selected_category.first().get_descendants(include_self=True)]

        first_part = products_for_homepage.distinct()[:4]
        second_part = None
        three_part = None
        four_part = None

        if products_for_homepage.count() > 4:
            second_part = products_for_homepage.distinct()[4:8]
        if products_for_homepage.count() > 8:
            three_part = products_for_homepage.distinct()[8:12]

        if products_for_homepage.count() > 12:
            four_part = products_for_homepage[12:16]

        if selected_category.count() > 1:
            # second product slider
            second_items = Product.objects.filter(
                category__in=[index.id for index in selected_category[1].get_descendants(include_self=True)]).distinct()

        if selected_category.count() > 2:
            # second product slider
            three_items = Product.objects.filter(
                category__in=[index.id for index in selected_category[2].get_descendants(include_self=True)]).exclude(
                Q(id__in=second_items.values('id')) | Q(id__in=first_part.values('id'))).distinct()

        special_offer_banner = SpecialOfferBanner.objects.order_by('?').first()
        advantages = OurAdvantages.objects.all()
        abouts_list = AboutUs.objects.filter(is_main=False)
        blog = Blog.objects.order_by('-id')[:3]

        context = {
            'first_part': first_part,
            'second_part': second_part,
            'reviews': reviews,
            'four_part': four_part,
            'three_part': three_part,
            'abouts_list': abouts_list,
            'homepage_about': homepage_about,
            'homepage_text': homepage_text,
            'slider_items': slider_items,
            'category_icons': category_icons,
            'selected_category': selected_category,
            'advantages': advantages,
            'machanents_videos': machanents_videos,
            'special_offer_banner': special_offer_banner,
            'posts': blog,
            'donation_currencies': donation_currencies,
            'donation_amounts': donation_amounts,
            'donation_homepage_content': donation_homepage_content,
        }
        # if second_items:
        #     context.update({'second_items': second_items[:4], 'second_category': selected_category[1]})

        # if three_items:
        #     context.update({'three_items': three_items[:4], 'three_category': selected_category[2]})
        return render(request, 'shop/index.html', context)


class CategoryView(generic.DetailView):
    """ Category detail view """
    model = Category
    queryset = Category.objects.all()
    slug_field = 'slug'
    template_name = 'shop/shop.html'
    context_object_name = 'category'

    def filter_products(self, products):
        url_kwargs = {}
        request = self.request
        for item in request.GET:
            if len(request.GET.getlist(item)) > 1:
                url_kwargs[item] = request.GET.getlist(item)
            else:
                url_kwargs[item] = request.GET.get(item)

        q_condition_queries = []
        two_input_field_names = []
        two_input_fields = FilterField.objects.filter(show_in_filters=True, two_inputs=True)

        for i in two_input_fields:
            two_input_field_names.extend(
                (f'min_{i.filter_key}', f'max_{i.filter_key}')
            )
        names_list = ['min_price', 'max_price', 'page', 'sorting', *two_input_field_names]

        for key, value in url_kwargs.items():
            if key not in names_list:
                if isinstance(value, list):
                    if (key == 'color'):
                        q_condition_queries.append(
                            {'color__title__in': value})
                    else:
                        q_condition_queries.append(
                            {f'productfeature__field__filter_key': key, 'productfeature__value__title__in': value})
                else:
                    if (key == 'color'):
                        q_condition_queries.append(
                            {'color__title': value})
                    else:
                        q_condition_queries.append(
                            {'productfeature__value__title': value, 'productfeature__field__filter_key': key})

        if request.GET.get('min_price'):
            min_price = floatformat(
                convert(int(request.GET.get('min_price')) - 1, request.session['currency'], 'AMD', decimals=0), 0)
            products = products.filter(finally_price__gte=int(min_price) - 1)
        if request.GET.get('max_price'):
            max_price = floatformat(
                convert(int(request.GET.get('max_price')) + 1, request.session['currency'], 'AMD', decimals=0), 0)
            products = products.filter(finally_price__lte=int(max_price))

        if len(q_condition_queries):
            for filter_item in q_condition_queries:
                products = products.filter(**filter_item).distinct()
        if request.GET.get('sorting'):
            products = products.order_by(request.GET.get('sorting'))
        else:
            products = products.order_by('-id')

        split_two_input_names = list(map(lambda x: x.split('_', 1)[-1], two_input_field_names))
        two_input_condition_list = []

        for k, v in url_kwargs.items():
            if k in two_input_field_names:
                pref, keyname = k.split('_', 1)
                suffix = ''
                if pref == 'min':
                    suffix = '__gte'
                elif pref == 'max':
                    suffix = '__lte'

                two_input_condition_list.append(
                    {'productfeature__field__filter_key': keyname,
                     f'productfeature__value__title{suffix}': v
                     }
                )

        if two_input_condition_list:
            for i in two_input_condition_list:
                products = products.filter(**i)

        # Pagination of products the current category
        paginator = Paginator(products.distinct(), 12)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)

        return {'page_obj': page_obj}

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)

        # Product list of the category
        list_ids_cat = [index.id for index in self.get_object().get_descendants(include_self=True)]
        products = Product.objects.filter(Q(category__in=list_ids_cat)).order_by('-id')

        # Product filtering
        context['filter_fields'] = FilterField.objects.filter(Q(productfeature__product__category__in=list_ids_cat),
                                                              Q(show_in_filters=True, two_inputs=False),
                                                              Q(productfeature__value__isnull=False)).distinct()

        context['featured_values'] = FilterValue.objects.filter(Q(productfeature__product__category__in=list_ids_cat) |
                                                                Q(productfeature__field__show_in_filters=True),
                                                                Q(productfeature__value__isnull=False)).distinct()
        context['colors'] = Color.objects.filter(Q(product__category__in=list_ids_cat)).distinct()
        filter_qs = self.filter_products(products)
        context['page_obj'] = filter_qs['page_obj']
        context['min_price_val'] = products.aggregate(min_price=Min('finally_price'))['min_price'] or 0
        context['max_price_val'] = products.aggregate(min_price=Max('finally_price'))['min_price'] or 0
        context['source_cats'] = self.get_object().get_ancestors(include_self=False).filter(
            parent=None) or self.get_object().children.all()
        two_input_fields = FilterField.objects.filter(Q(productfeature__product__category__in=list_ids_cat),
                                                              Q(show_in_filters=True, two_inputs=True),
                                                              Q(productfeature__value__isnull=False)).distinct()
        context.update({'two_input_fields': two_input_fields})
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        list_ids_cat = [index.id for index in self.get_object().get_descendants(include_self=True)]
        products = Product.objects.filter(Q(category__in=list_ids_cat)).order_by('-id')
        if self.request.is_ajax():
            filter_result = self.filter_products(products)

            resp = {
                'data': render_to_string('includes/filtered_item.html', {'page_obj': filter_result['page_obj'],
                                                                         'request': self.request}, request=self.request)
            }
            return JsonResponse(resp, status=200)

        return super().get(request, *args, **kwargs)


class ProductView(DetailView):
    """ Product detail view """

    model = Product
    slug_field = 'slug'
    template_name = 'shop/product_page.html'
    context_object_name = 'obj'

    def generate_last_viewed(self):
        """ At first we check is there  list of viewed products  in the db regarded given session key
            if there not, we create list with that key 
        """

        product = self.get_object()
        session_key = self.request.session.session_key

        if not session_key:
            session_key = self.request.session.cycle_key

        viewed_list, _ = ViewedProducts.objects.get_or_create(session_key=session_key)
        if product.id not in viewed_list.products.all():
            viewed_list.products.add(product.id)
            viewed_list.save()
        return viewed_list.products.exclude(id=product.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        try:
            latest_visited_cat = self.request.META.get('HTTP_REFERER').split('/')[-2]
            bred_category = Category.objects.get(slug=latest_visited_cat)
        except:
            bred_category = Category.objects.filter(product__slug__iexact=self.get_object().slug).first()

        list_ids_cat = [index.id for index in bred_category.get_descendants(include_self=True)]

        # Related items list
        sort_array = ['created_at', '-created_at', '-price', 'price', 'title', 'sale']
        random.shuffle(sort_array)
        context['related_items'] = Product.objects.filter(Q(category__in=list_ids_cat), ~Q(id=product.id)).order_by(
            sort_array[0]).distinct()[:16]
        # Latest seen products
        context['variant_fields'] = FilterField.objects.filter(productfeature__product_id=product.id, is_main=True,
                                                               productfeature__value__isnull=False).distinct()
        context['variant_values'] = product.productfeature_set.filter(field__is_main=True).order_by('price')
        # .values('productfeature__value__title',
        #                                                              'productfeature__price', 'id',
        #                                                              'productfeature__id', 'filter_key')
        context['features'] = product.productfeature_set.filter(field__is_main=False)

        context['main_fields'] = ProductFeature.objects.filter(product_id=product.id)
        context['last_seen'] = self.generate_last_viewed().exclude(id__in=context['related_items'].values('id'))

        context['ratings'] = Rating.objects.order_by('-value')

        context['middle_score'] = RatingProduct.objects.filter(product_id=product.id).aggregate(
            middle=Avg('rating__value'))
        context['middle'] = float('{:.1f}'.format(context['middle_score'].get('middle') or 0))
        context['user_block'] = RatingProduct.objects.filter(ip=get_ip_client(self.request),
                                                             product_id=product.id).exists()
        context['user_rating'] = None
        if context['user_block']:
            context['user_rating'] = RatingProduct.objects.get(ip=get_ip_client(self.request),
                                                               product_id=product.id).rating
        # Rating
        context['bred_category'] = bred_category
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)

@csrf_exempt
def create_rating(request):
    if request.method == 'GET':
        return HttpResponse(status=405, content={"detail": 'Method not allowed'})

    data = json.loads(request.body)
    rating_id = data.get('rating')
    rating_id = Rating.objects.get(value=rating_id)
    product_id = data.get('product')
    try:
        product_rating, _ = RatingProduct.objects.update_or_create(product_id=product_id,
                                                                   ip=get_ip_client(request),
                                                                   defaults={'rating_id': rating_id.id}
                                                                   )


    except Exception as e:
        return HttpResponse(status=400)

    middle_score = RatingProduct.objects.filter(product_id=product_id).aggregate(middle=Avg('rating__value'))
    middle = float('{:.1f}'.format(middle_score.get('middle')))
    return JsonResponse({'success': 'Rating created', 'rating': middle})


class CatalogView(View):
    """ Catalog view """

    def get(self, request, **kwargs):
        bread_content = BreadcrumbTexts.objects.filter(location='categories').first()
        categories = Category.objects.filter(parent=None)
        return render(request, 'shop/catalog.html', {'categories': categories, 'bread_content': bread_content})


class TermsAndConditionsView(generic.TemplateView):
    template_name = 'shop/terms_and_conditions.html'

    def get_context_data(self, **kwargs):
        context = super(TermsAndConditionsView, self).get_context_data(**kwargs)
        context['terms_and_cond'] = TermsAndConditions.objects.last()
        return context


class PrivacyPolicyView(generic.TemplateView):
    template_name = 'shop/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
        context['privacy_policy'] = PrivacyPolicy.objects.last()
        return context


class DeliveryAndPaymentView(generic.TemplateView):
    template_name = 'shop/delivery_and_payment.html'

    def get_context_data(self, **kwargs):
        context = super(DeliveryAndPaymentView, self).get_context_data(**kwargs)
        context['del_and_pay'] = DeliveryAndPayMent.objects.last()
        return context


class SearchListView(View):
    template_name = 'shop/search.html'

    def get_queryset(self):
        qs = Product.objects.all()
        if q := self.request.GET.get('q'):
            qs = qs.filter(Q(title__icontains=q) | Q(slug__icontains=q) | Q(product_code__contains=q))

        return qs

    @never_cache
    def get(self, request, **kwargs):
        q = self.request.GET.get('q')
        products = self.get_queryset()
        if request.GET.get('sorting'):
            products = products.order_by(request.GET.get('sorting'))
        paginator = Paginator(products.distinct(), 12)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        bread_content = BreadcrumbTexts.objects.filter(location='search').first()
        if request.is_ajax():
            sorting = request.GET.get('sorting')
            paginator = Paginator(self.get_queryset().order_by(sorting).distinct(), 12)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            resp = {
                'data': render_to_string('includes/filtered_item.html', {'page_obj': page_obj,
                                                                         'request': self.request}, request=request)
            }
            return JsonResponse(resp, status=200)

        return render(request, self.template_name,
                      {'page_obj': page_obj,
                       'products': self.get_queryset(),
                       'bread_content': bread_content
                       })


def ajaxSearch(request):
    data = request.GET.get('q')

    return_dict = {'products': []}
    if data:
        products = Product.objects.filter(
            Q(title__icontains=data) | Q(slug__icontains=data) | Q(product_code__contains=data)).order_by('?')[:10]
        for product in products:
            new_dict = {'name': product.title, 'image': product.main_photo.url, 'slug': product.get_absolute_url()}

            return_dict['products'].append(new_dict)
    return JsonResponse(return_dict)


class ProductListView(ListView):
    paginate_by = 12
    template_name = 'shop/sale.html'
    queryset = Product.objects.order_by('-id')

    def get_queryset(self):
        qs = self.queryset
        query_param = self.request.GET.get('type')
        if query_param == 'new':
            qs = qs.order_by('-id')
        if query_param == 'sale':
            qs = qs.filter(sale__gt=0)
        if query_param == 'best_seller':
            qs = qs.filter(best_seller=True)
        else:
            qs = qs.order_by('-id')
        return qs

    def get(self, request, **kwargs):
        products = self.get_queryset()
        if request.GET.get('sorting'):
            products = products.order_by(request.GET.get('sorting'))
        paginator = Paginator(products.distinct(), 12)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        if request.is_ajax():
            sorting = request.GET.get('sorting')
            paginator = Paginator(self.get_queryset().order_by(sorting).distinct(), 12)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            resp = {
                'data': render_to_string('includes/filtered_item.html', {'page_obj': page_obj,
                                                                         'request': self.request}, request=request)
            }
            return JsonResponse(resp, status=200)

        context = {'page_obj': page_obj}

        if request.GET.get('type') in ['new', 'sale', 'best_seller']:
            if request.GET.get('type') == 'new' or not request.GET.get('type'):
                context['bread_content']: BreadcrumbTexts = BreadcrumbTexts.objects.filter(
                    location='new_products').first()
            if request.GET.get('type') == 'sale':
                context['bread_content']: BreadcrumbTexts = BreadcrumbTexts.objects.filter(location='sale').first()
            if request.GET.get('type') == 'best_seller':
                context['bread_content']: BreadcrumbTexts = BreadcrumbTexts.objects.filter(
                    location='best_seller').first()
            return render(request, self.template_name, context)

        return redirect(reverse('offers') + '?type=new')


class AllProductListView(View):

    def get(self, request, **kwargs):
        products = Product.objects.all().order_by('-id').distinct()
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        view_name = "all_products"

        context = {
            "page_obj": page_obj,
            "view_name": view_name

        }
        return render(request, 'shop/search.html', context)


def authors(request):
    author_list = Authors.objects.all()
    author_categories = AuthorCategories.objects.all()
    bread_content = BreadcrumbTexts.objects.filter(location='authors').first()

    pagination = Paginator(author_list, 12)
    page = request.GET.get('page', 1)
    page_obj = pagination.get_page(page)

    context = {
        'page_obj': page_obj,
        'author_categories': author_categories,
        'bread_content': bread_content
    }
    return render(request, 'flatpages/authors.html', context)


def author_categories(request, slug):
    category = get_object_or_404(AuthorCategories, slug=slug)
    items = Authors.objects.filter(category=category)
    author_categories = sorted(AuthorCategories.objects.all(), key=lambda x: x.id == category.id, reverse=True)

    pagination = Paginator(items, 12)
    page = request.GET.get('page', 1)
    page_obj = pagination.get_page(page)

    context = {
        'page_obj': page_obj,
        'category': category,
        'author_categories': author_categories,
    }

    return render(request, 'flatpages/authors_category.html', context)


def author_details(request, slug):
    author = get_object_or_404(Authors, slug=slug)
    items = Product.objects.filter(author=author)

    context = {
        'author': author,
        'items': items
    }
    return render(request, 'flatpages/author_details.html', context)


def reviews_list(request):
    return render(request, 'flatpages/reviews.html')
