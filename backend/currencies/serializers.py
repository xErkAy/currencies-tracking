from rest_framework import serializers

from currencies.exceptions import CurrencyDoesNotExist
from currencies.models import (
    Currency,
    CurrencyHistory,
    TrackingCurrency
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CurrencyHistorySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = CurrencyHistory
        fields = '__all__'


class TrackingCurrencySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = TrackingCurrency
        exclude = ('user',)


class TrackingCurrencySerializerWithDate(serializers.Serializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        currency = Currency.objects.get(id=instance.currency.id)
        history = CurrencyHistory.objects.get(currency_id=instance.currency.id, date=self.context.get('date'))
        return {
            'currency': CurrencySerializer(currency).data,
            'currency_value': history.value,
            'limit': instance.limit,
            'is_greater': True if history.value > instance.limit else False
        }


class CreateTrackingCurrencySerializer(serializers.Serializer):
    currency_id = serializers.IntegerField()
    limit = serializers.FloatField()


class CurrencyAnalyticsQueryParamsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    currency_id = serializers.IntegerField()
    limit = serializers.FloatField()


class CurrencyAnalyticsSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()

    @staticmethod
    def get_value_relation(value, limit):
        if value > limit:
            return 'greater'
        elif value < limit:
            return 'lower'
        else:
            return 'equals'

    def get_result(self, instance):
        return {
            instance.date.strftime('%Y-%m-%d'): {
                'date': instance.date.strftime('%Y-%m-%d'),
                'value': instance.value,
                'result': self.get_value_relation(instance.value, self.context.get('limit'))
            }
        }

    def get_data(self, instance):
        history = CurrencyHistory.objects.filter(
            currency_id=instance.id,
            date__range=(self.context.get('start_date'), self.context.get('end_date'))
        )

        result = [self.get_result(i) for i in history]

        return result


class CurrencyAnalyticsHistorySerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        return {
            'date': instance.date,
            'is_greater': True if instance.value > self.context.get('limit') else False
        }
