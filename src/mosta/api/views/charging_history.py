from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwnerOfIssuer
from mosta.api.serializers.charging_history import ChargingHistorySerializer, ChargingCreateHistorySerializer
from mosta.phone.models import ChargingHistory


class ChargingHistoryViewSet(viewsets.ModelViewSet):
    queryset = ChargingHistory.objects.all()
    serializer_class = ChargingHistorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfIssuer
    )
    http_method_names = ('get', 'post')

    def get_queryset(self):
        return ChargingHistory.objects.filter(issuer__owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChargingCreateHistorySerializer
        return self.serializer_class
