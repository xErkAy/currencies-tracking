# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('swagger/', get_schema_view(title='API Docs', authentication_classes=()), name='api_schema'),
    path('docs/', TemplateView.as_view(template_name='docs.html',
                                       extra_context={'schema_url': 'api_schema'}
                                       ), name='api_docs'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/tests/', include('tests.urls')),
    path('api/currencies/', include('currencies.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
