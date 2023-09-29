# -*- coding: utf-8 -*-
import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from currencies.models import Currency
from project.serializers import CurrencyInstance
from project.utils import _print

logger = logging.getLogger('fill_up_currencies')


class Command(BaseCommand):

    def handle(self, *args, **options):
        _print(logger, 'Started filling currencies info')

        data = self._get_currencies_info()
        if data is None:
            return

        currencies_list = data.get('Valute')

        objects_to_create = []
        for currency in currencies_list:
            serialized_data = CurrencyInstance(currencies_list[currency])

            objects_to_create.append(
                Currency(
                    external_id=serialized_data.id,
                    num_code=serialized_data.num_code,
                    name=serialized_data.name,
                    char_code=serialized_data.char_code
                )
            )

        Currency.objects.bulk_create(objects_to_create)

        _print(logger, f'Finished. Added the information about {len(objects_to_create)} currencies.')

    @staticmethod
    def _get_currencies_info():
        try:
            response = requests.get(settings.TODAY_CURRENCIES_URL).json()
            return response
        except:
            _print(logger, f'Something went wrong. Canceling... The error is: {str(e)}', is_error=True)
            return None
