# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def money(value):
    """Converts a price into local currency format"""
    if settings.CURRENCY == 'UAH':
        return str(value) + ' грн'
    else:
        return "$ " + str(value)
