from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from core.utils import CustomModel, slug_generator


class StaticPages(CustomModel):
    page_title = models.CharField(max_length=160, verbose_name="Էջի վերնագիր")
    text = RichTextUploadingField(verbose_name="Տեքստ")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Հղում")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Դասավորել")

    class Meta:
        ordering = ['my_order']
        verbose_name = "Ստատիկ էջ"
        verbose_name_plural = "Ստատիկ էջեր"

    def __str__(self):
        return self.page_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.page_title, self.__class__)
            
        super(StaticPages, self).save(*args, **kwargs)

