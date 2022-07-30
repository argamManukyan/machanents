from django.db import models

from core.utils import CustomModel, CustomLogoField

TEXT_LOCATION = [
    # ('catalog', 'Տեսականի'),
    ('sale', 'Ակցիա'),
    ('new_products', 'Նորույթ'),
    ('best_seller', 'Հատուկ առաջարկ'),
    ('categories', 'Բաժինների էջ'),
    # ('brands', 'Բրենդների էջ'),
    ('blog', 'Բլոգ'),
    # ('gallery', 'Տեսադարան'),
    # ('contacts', 'Կապ'),
    ('authors', 'Արտիստներ'),
    # ('faq', "Հաճախակի տրվող հարցեր"),
    ('machanents_tv', 'Machanents TV')
]


class BreadcrumbTexts(CustomModel):
    """ Breadcrumb texts and images """
    location = models.CharField(choices=TEXT_LOCATION, max_length=150, unique=True, verbose_name='Ընտրեք էջը')
    breadcrumbs_text = models.TextField(blank=True, null=True, verbose_name='Breadcrumb -ի տեքստ')
    breadcrumbs_image = CustomLogoField(blank=True, null=True, verbose_name='Breadcrumb -ի Նկար')
    # page_title = models.CharField(max_length=255, blank=True, verbose_name='Էջի վերնագիր')

    def __str__(self):
        return f'{self.get_location_display()}'

    class Meta:
        verbose_name = 'Breadcrumb -ի կոնտենտ'
        verbose_name_plural = verbose_name



