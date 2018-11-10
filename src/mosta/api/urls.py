from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from mosta.api.views.balance_history import BalanceHistoryViewSet
from mosta.api.views.call_history import CallHistoryViewSet
from mosta.api.views.charging_history import ChargingHistoryViewSet
from mosta.api.views.phone import PhoneViewSet
from mosta.api.views.sim import SimViewSet
from mosta.api.views.sms import SMSViewSet
from mosta.api.views.power_socket import PowerSocketViewSet

router = DefaultRouter()
router.register(r'phone', PhoneViewSet)
router.register(r'balance_history', BalanceHistoryViewSet)
router.register(r'charging_history', ChargingHistoryViewSet)
router.register(r'call_history', CallHistoryViewSet)
router.register(r'sim', SimViewSet)
router.register(r'sms', SMSViewSet)
router.register(r'socket', PowerSocketViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
