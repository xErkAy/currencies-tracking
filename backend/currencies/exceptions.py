from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class CurrencyDoesNotExist(APIException):
    default_code = 400
    default_detail = _('Requested currency does not exist')


class TrackingCurrencyAlreadyExists(APIException):
    default_code = 400
    default_detail = _('You are already tracking this currency')
