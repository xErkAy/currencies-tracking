from django.contrib import admin
from project.models import User
from currencies.models import (
    Currency,
    CurrencyHistory,
    TrackingCurrency
)

admin.site.register(User)
admin.site.register(Currency)
admin.site.register(CurrencyHistory)
admin.site.register(TrackingCurrency)

