from django.forms import ModelForm


from .models import ProductReviews


class ProductReviewsForm(ModelForm):
    class Meta:
        model = ProductReviews
        fields = '__all__'
