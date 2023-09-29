from django.urls import path
from currencies.views import (
    GetTrackingCurrencies,
    CreateUpdateTrackingCurrency,
    CurrencyAnalytics
)

urlpatterns = [
    path('list/', GetTrackingCurrencies.as_view()),
    path('create/', CreateUpdateTrackingCurrency.as_view()),
    path('analytics/', CurrencyAnalytics.as_view()),
]
