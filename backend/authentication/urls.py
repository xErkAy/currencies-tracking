# -*- coding: utf-8 -*-
from django.urls import path
from authentication.views import AuthenticationAPIView, RegistrationAPIView

urlpatterns = [
    path('', AuthenticationAPIView.as_view(), name='user_auth'),
    path('registration/', RegistrationAPIView.as_view(), name='user_registration'),
]
