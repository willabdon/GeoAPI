from django.db import models


class Provider(models.Model):
    name = models.CharField('Name', max_length=255)
    email = models.CharField('Email', max_length=255)
    phone = models.CharField('Phone', max_length=15)
    language = models.CharField('language', max_length=35)
    currency = models.CharField('currency', max_length=3)
