from django.urls import path
from tests.views import TestAPIView

urlpatterns = [
    path('auth/', TestAPIView.as_view(), name='test_auth')
]
