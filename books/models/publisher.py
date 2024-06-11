from django.db import models
from django.utils.translation import gettext_lazy as _


class Publisher(models.Model):
    class Category(models.TextChoices):
        GENERAL = 'GE', _('GENERAL')
        SCIENCE = 'SC', _('SCIENCE')
        TRADE = 'TR', _('TRADE')
        EDUCATIONAL = 'ED', _('EDUCATIONAL')

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.GENERAL)

    def __str__(self):
        return self.name
