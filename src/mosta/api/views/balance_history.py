from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwnerOfSim
from mosta.api.serializers.balance_history import BalanceHistorySerializer, BalanceHistoryCreateSerializer
from mosta.phone.models import BalanceHistory


class BalanceHistoryViewSet(viewsets.ModelViewSet):
    queryset = BalanceHistory.objects.all()
    serializer_class = BalanceHistorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfSim
    )
    http_method_names = ('get', 'post')

    def get_queryset(self):
        return BalanceHistory.objects.filter(sim__owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BalanceHistoryCreateSerializer
        return self.serializer_class
