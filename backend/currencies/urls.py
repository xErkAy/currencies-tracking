from django.urls import path
from currencies.views import (
    GetTrackingCurrencies,
    CreateTrackingCurrency,
    CurrencyAnalytics
)

urlpatterns = [
    path('list/', GetTrackingCurrencies.as_view()),
    path('create/', CreateTrackingCurrency.as_view()),
    path('analytics/', CurrencyAnalytics.as_view()),
]
