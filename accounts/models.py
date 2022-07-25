from django.db import models
from django.contrib.auth.models import User
from order.models import Countries, Regions


class Profile(models.Model):
    """ Custom user model """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True)

    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.first_name


