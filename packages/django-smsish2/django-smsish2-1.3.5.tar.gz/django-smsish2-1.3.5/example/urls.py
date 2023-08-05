from django.conf import settings
from django.urls import path, include
from django.contrib import admin

import django_rq.urls

urlpatterns = [
    path("admin/", admin.site.urls),
]

if 'django_rq' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('django-rq/', include('django_rq.urls')),
    ]
