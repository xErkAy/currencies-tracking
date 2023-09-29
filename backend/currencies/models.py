# -*- coding: utf-8 -*-
from django.db import models

from project.models import User


class Currency(models.Model):
    external_id = models.CharField(max_length=10)
    num_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    char_code = models.CharField(max_length=10)

    def __str__(self):
        return f'[{self.char_code}] {self.name}'

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class CurrencyHistory(models.Model):
    currency = models.ForeignKey(Currency, related_name='history', on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()

    def __str__(self):
        return f'[{self.date}] {self.currency.name} - {self.value}'

    class Meta:
        verbose_name = 'Currency history'
        verbose_name_plural = 'Currency histories'


class TrackingCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    limit = models.FloatField()

    def __str__(self):
        return f'[{self.user}] {self.currency.name} - {self.limit}'

    class Meta:
        verbose_name = 'Tracking currency'
        verbose_name_plural = 'Tracking currencies'
