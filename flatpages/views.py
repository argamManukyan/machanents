from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from flatpages.forms import ContactForm, ServiceForm
from shop.models import OurAdvantages
from django.urls import reverse
from .models import AboutUs, Blog, Gallery, GalleryCategory, FAQ, Service, BlogCategory, AboutUsSocialIcons
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from breadcrumbs.models import BreadcrumbTexts


class AboutUsView(View):
    """ About us view """

    def get(self, request, **kwargs):
        about_us: AboutUs = AboutUs.objects.filter(is_main=True).first()
        about_us_items = AboutUs.objects.exclude(id=about_us.id)
        about_us_social_icons = AboutUsSocialIcons.objects.all()
        context = {
            'about_us': about_us,
            'about_us_items': about_us_items,
            'about_us_social_icons': about_us_social_icons,
        }
        return render(request, 'flatpages/about_us.html', context)


class AboutUsCategoryView(View):
    def get(self, request, **kwargs):
        about_us: AboutUs = get_object_or_404(AboutUs, slug=kwargs['slug'])

        about_us_items = AboutUs.objects.exclude(id=about_us.id)
        about_us_social_icons = AboutUsSocialIcons.objects.all()
        context = {
            'about_us': about_us,
            'about_us_items': about_us_items,
            'about_us_social_icons': about_us_social_icons,
        }
        return render(request, 'flatpages/about_us.html', context)


class FAQView(ListView):
    model = FAQ
    queryset = FAQ.objects.all()
    template_name = 'flatpages/faq.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bread_content'] = BreadcrumbTexts.objects.filter(location='faq').first()
        return context


class GalleryListView(ListView):
    model = Gallery
    template_name = 'flatpages/gallery.html'
    context_object_name = 'galleries'
    queryset = Gallery.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['bread_content'] = BreadcrumbTexts.objects.filter(location='gallery').first()
        context['categories'] = GalleryCategory.objects.all()

        paginator = Paginator(Gallery.objects.all(), 24)
        page = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page)
        return context


class GalleryCategoryDetailView(DetailView):
    model = GalleryCategory
    template_name = 'flatpages/gallery_details.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(GalleryCategoryDetailView, self).get_context_data(**kwargs)
        context['images'] = Gallery.objects.filter(category_id=self.get_object().id)
        context['categories'] = GalleryCategory.objects.all()
        paginator = Paginator(context['images'], 24)
        page = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page)
        return context


class BLogListView(ListView):
    model = Blog
    template_name = 'flatpages/blog.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bread_content'] = BreadcrumbTexts.objects.filter(location='blog').first()
        context['categories'] = BlogCategory.objects.all()
        return context


class BlogCategoryDetailView(View):

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(BlogCategory, slug=kwargs['slug'])
        categories = sorted(BlogCategory.objects.all(), key=lambda x: x.id == category.id, reverse=True)
        posts = Blog.objects.filter(category=category).distinct()

        paginator = Paginator(posts, 12)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'category': category,
            'categories': categories,
        }

        return render(request, 'flatpages/blog_category.html', context)


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'flatpages/blog_full.html'
    lookup_field = 'slug'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        post = self.get_object()

        if post.slug not in request.session:
            request.session[post.slug] = post.slug
            post.views_count += 1
            post.save()

        return super().get(request, *args, **kwargs)


class ServiceListView(ListView):
    model = Service
    template_name = 'flatpages/services.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bread_content'] = BreadcrumbTexts.objects.filter(location='service').first()
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'flatpages/services-full.html'
    lookup_field = 'slug'
    context_object_name = 'service'

    def post(self, request, **kwargs):
        form = ServiceForm(request.POST, None)
        if form.is_valid():
            data = dict(form.cleaned_data)
            messages.success(request,
                             _('Ձեր հայտը հաջողությամբ ուղարկված է:<br />Մեր մենեջերը շուտով կապ կհաստատի Ձեզ հետ:'))
            return redirect(reverse('service_details', kwargs={'slug': self.get_object().slug}))
        else:
            messages.error(request, _('Տեղի է ունեցել սխալ:<br />Խնդրում ենք փորձել մի փոքր ուշ:'))
            return redirect(reverse('service_details', kwargs={'slug': self.get_object().slug}))
