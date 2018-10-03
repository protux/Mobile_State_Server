from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from mosta.api.views.phone import PhoneViewSet

router = DefaultRouter()
router.register(r'phone', PhoneViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
