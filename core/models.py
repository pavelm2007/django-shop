from django.db import models

class Setting(models.Model):
    CURRENCY_LIST = (
        ('USD', 'USA dollars'),
        ('EUR', 'Euro'),
        ('UAH', 'Ukrainian hryvnia'),
        ('RUB', 'Russian ruble'),
        )

    image = models.ImageField(upload_to="core/", null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_LIST, default="USA")
    is_active = models.BooleanField(default=True)