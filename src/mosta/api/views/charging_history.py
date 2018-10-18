from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwnerOfIssuer
from mosta.api.serializers.charging_history import ChargingHistorySerializer
from mosta.phone.models import ChargingHistory


class ChargingHistoryViewSet(viewsets.ModelViewSet):
    queryset = ChargingHistory.objects.all()
    serializer_class = ChargingHistorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfIssuer
    )
    http_method_names = ('get',)

    def get_queryset(self):
        return ChargingHistory.objects.filter(issuer__owner=self.request.user)
