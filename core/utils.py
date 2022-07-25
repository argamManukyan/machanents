""" There is written all utils """
import time
from functools import wraps
from unidecode import unidecode
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify


def generic_context_processor(model, excluded_items: dict = None, filter_items: dict = None):
    """ decorator for returning custom context processors """
    print(model)
    @wraps
    def inner(func):
        def wrapper(*args, **kwargs):
            print(func(*args, **kwargs))
            qs = model.objects.all()
            if filter_items:
                qs =qs.filter(**filter_items)

            if excluded_items:
                qs = qs.exclude(**excluded_items)
            print(kwargs)
            return {func.__name__: qs}

        return wrapper

    return inner


class CustomModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomMetaModel(CustomModel):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    #
    # def __init__(self, **kwargs):
    #     super(CustomMetaModel, self).__init__(**kwargs)
    #     try:
    #         from mptt.models import MPTTModel, TreeForeignKey
    #         test = MPTTModel in self.__class__.mro()
    #     except:
    #         test = False
    #
    #     if not test:
    #         self.__class__.my_order = models.PositiveIntegerField(default=0)
    #         self._meta.ordering = ['-my_order']

    class Meta:
        abstract = True

class CustomLogoField(models.FileField):
    validators = [FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'webp', 'mp4', 'waw'])]
    null = True
    blank = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'verbose_name' not in kwargs:
            self.verbose_name = 'Նկար'
        self.null = kwargs.get('null', self.null)
        self.blank = kwargs.get('blank', self.blank)


def slug_generator(title, model):
    last_id = model.objects.order_by('-id').first().id + 1 if model.objects.count() else 1
    return slugify(unidecode(title) + '-' + str(last_id))


def smart_strip(text):
    """ Function for strip filter fields for correct showing """
    spl_str = text.split(' ')
    new_str = ' '.join(list(filter(lambda x: len(x) > 0, spl_str)))
    return new_str