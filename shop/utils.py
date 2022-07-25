from django.db import models


class CustomModel(models.Model):
    """ Custom abstract model for templating each of models """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True