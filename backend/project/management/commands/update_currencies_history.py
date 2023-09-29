# -*- coding: utf-8 -*-
import logging
import time

import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from currencies.models import Currency, CurrencyHistory
from project.serializers import CurrencyInstance
from project.utils import _print

logger = logging.getLogger('update_currencies_history')


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.objects_to_create = []
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        _print(logger, 'Started updating info about currencies')

        try:
            response = requests.get(settings.TODAY_CURRENCIES_URL).json()
            date = response.get('Date').split('T')[0]
            prev_url = 'https:' + response.get('PreviousURL').replace('archive', 'archive/')

            if not CurrencyHistory.objects.filter(date=date).exists():
                self._add_currency_history(response.get('Valute'), date)
                _print(logger, f'Added currencies info on {date}')

            for _ in range(30):
                for _ in range(10):
                    response = requests.get(prev_url).json()
                    date = response.get('Date')
                    if date is not None:
                        date = date.split('T')[0]
                        break
                    time.sleep(1)
                if date is None:
                    _print(logger, 'The site is unavailable. Canceling..', is_error=True)

                prev_url = 'https:' + response.get('PreviousURL').replace('archive', 'archive/')

                if not CurrencyHistory.objects.filter(date=date).exists():
                    self._add_currency_history(response.get('Valute'), date)
                    _print(logger, f'Added currencies info on {date}')

        except Exception as e:
            _print(logger, f'Something went wrong. Canceling...', is_error=True)
            _print(logger, str(e), is_error=True)
            return

        CurrencyHistory.objects.bulk_create(self.objects_to_create)
        _print(logger, f'Finished. Added {len(self.objects_to_create)} history information about currencies')

    def _add_currency_history(self, currencies_list: list, date: str):
        for currency in currencies_list:
            serialized_data = CurrencyInstance(currencies_list[currency])

            try:
                currency = Currency.objects.get(char_code=serialized_data.char_code)
            except Currency.DoesNotExist:
                currency = self._create_currency(serialized_data)

            self.objects_to_create.append(
                CurrencyHistory(
                    currency=currency,
                    date=date,
                    value=format(serialized_data.value / serialized_data.nominal, '.4f')
                )
            )

    @staticmethod
    def _create_currency(instance: CurrencyInstance):
        return Currency.objects.create(
            external_id=instance.id,
            num_code=instance.num_code,
            name=instance.name,
            char_code=instance.char_code
        )
