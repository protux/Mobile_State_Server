"""mosta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from mosta.pages.views import RedirectHomepageOrDashboardView

urlpatterns = i18n_patterns(
    url(r'^$', RedirectHomepageOrDashboardView.as_view()),
    url(r'^phone/', include('mosta.phone.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^pages/', include('mosta.pages.urls')),
    url(r'^dashboard/', include('mosta.dashboard.urls')),
    path('admin/', admin.site.urls),
)
urlpatterns += [
    url(r'^api/', include('mosta.api.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
