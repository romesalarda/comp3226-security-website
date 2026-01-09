"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.urls import path, include
import logging


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    
]
try:
    from django_rest_opaque.urls import get_url_patterns as get_opaque_urlpatterns

    urlpatterns.append(
        path('o/', include((get_opaque_urlpatterns())))
    )

except (ImportError, ImproperlyConfigured) as e:
    logging.warning("django-rest-opaque is not installed or you haven't added the OPAQUE_SERVER_SETUP. Skipping OPAQUE authentication URLs.")
    logging.error("Orignal error: %s", e)