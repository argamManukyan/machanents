from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from breadcrumbs.models import BreadcrumbTexts
from .models import Video, VideoCategory


def video_category(request, slug):
    category = get_object_or_404(VideoCategory, slug=slug)
    video_categories = sorted(VideoCategory.objects.all(),
                              key=lambda x: x.id == category.id, reverse=True)

    videos = Video.objects.filter(category=category)
    page = request.GET.get('page', 1)
    paginator = Paginator(videos, 8)
    page_obj = paginator.get_page(page)

    context = {
        'category': category,
        'video_categories': video_categories,
        'page_obj': page_obj
    }
    return render(request, 'flatpages/machanents_tv_category.html', context)


def video_list(request):

    videos = Video.objects.all()

    bread_content: BreadcrumbTexts = BreadcrumbTexts.objects.filter(location='machanents_tv').first()

    video_categories = VideoCategory.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(videos, 8)
    page_obj: Video = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'bread_content': bread_content,
        'video_categories': video_categories
    }

    return render(request, 'flatpages/machanentsTV.html', context)



