from django.contrib.auth.models import AnonymousUser
from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.response import Response
from rest_framework.views import APIView

from currencies.exceptions import CurrencyDoesNotExist, TrackingCurrencyAlreadyExists
from currencies.models import (
    Currency,
    TrackingCurrency,
    CurrencyHistory
)
from currencies.serializers import (
    CurrencySerializer,
    CurrencyHistorySerializer,
    TrackingCurrencySerializer,
    CreateTrackingCurrencySerializer,
    TrackingCurrencySerializerWithDate,
    CurrencyAnalyticsQueryParamsSerializer, CurrencyAnalyticsSerializer
)


class GetTrackingCurrencies(APIView):

    @staticmethod
    def _get_sorting_value(params):
        sort = params.get('sort', None)
        if sort is not None:
            if sort == 'asc':
                return 'value'
            elif sort == 'desc':
                return '-value'
            else:
                return None

        return None

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization", ))
    def get(self, request, *args, **kwargs):
        sort = self._get_sorting_value(request.query_params)
        max_date = CurrencyHistory.objects.aggregate(Max('date')).get('date__max')

        if request.user is AnonymousUser:
            queryset = CurrencyHistory.objects.filter(date=max_date)
            if sort is not None:
                queryset = queryset.order_by(sort)
            return Response(CurrencyHistorySerializer(queryset, many=True).data)
        else:
            queryset = TrackingCurrency.objects.filter(user=request.user)
            if sort is not None:
                queryset = queryset.order_by(sort)
            return Response(TrackingCurrencySerializerWithDate(queryset, context={'date': max_date}, many=True).data)


class CreateTrackingCurrency(APIView):

    @staticmethod
    def _validate_data(data):
        serializer = CreateTrackingCurrencySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def post(self, request, *args, **kwargs):
        data = self._validate_data(request.data)

        try:
            currency_obj = Currency.objects.get(id=data.get('currency_id'))
        except Currency.DoesNotExist:
            raise CurrencyDoesNotExist()

        if TrackingCurrency.objects.filter(user=request.user, currency=currency_obj).exists():
            raise TrackingCurrencyAlreadyExists()

        obj = TrackingCurrency.objects.create(
            user=request.user,
            currency=currency_obj,
            limit=data.get('limit')
        )

        return Response(TrackingCurrencySerializer(obj).data)


class CurrencyAnalytics(APIView):

    @staticmethod
    def _validate_data(data):
        serializer = CurrencyAnalyticsQueryParamsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization", ))
    def get(self, request, *args, **kwargs):
        params = self._validate_data(request.query_params)

        try:
            currency = Currency.objects.get(id=params.get('currency_id'))
        except Currency.DoesNotExist:
            raise CurrencyDoesNotExist()

        return Response(CurrencyAnalyticsSerializer(currency, context=params).data)
