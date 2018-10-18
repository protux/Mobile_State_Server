from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwnerOfSim
from mosta.api.serializers.balance_history import BalanceHistorySerializer
from mosta.phone.models import BalanceHistory


class BalanceHistoryViewSet(viewsets.ModelViewSet):
    queryset = BalanceHistory.objects.all()
    serializer_class = BalanceHistorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfSim
    )
    http_method_names = ('get',)

    def get_queryset(self):
        return BalanceHistory.objects.filter(sim__owner=self.request.user)
