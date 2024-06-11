from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        DELIVERED = 'DV', _('DELIVERED')
        PENDING = 'PD', _('PENDING')
        SHIPPED = 'SP', _('SHIPPED')

    address = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DELIVERED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
