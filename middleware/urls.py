"""
URL configuration for middleware project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path

from . import settings
from core import views
from core.urls import core_urlpatterns
from original_message.urls import original_message_urlspatterns
from unit_message.urls import unit_message_urlspatterns
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    path('admin/', admin.site.urls),
    path('', include(core_urlpatterns)),
    path('original-message/', include(original_message_urlspatterns)),
    path('unit-message/', include(unit_message_urlspatterns)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, 
            document_root=settings.MEDIA_ROOT)
    
# Personalización del administrador de Django
admin.site.site_header = 'NetData Solutions'
admin.site.index_title = 'Panel de administración'
admin.site.site_title = 'NetData Solutions *'