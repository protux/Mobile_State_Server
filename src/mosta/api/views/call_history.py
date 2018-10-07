from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwner, IsOwnerOfSim
from mosta.api.serializers.call_history import CallHistorySerializer, CallHistoryCreateSerializer
from mosta.phone.models import CallHistory


class CallHistoryViewSet(viewsets.ModelViewSet):
    queryset = CallHistory.objects.all()
    serializer_class = CallHistorySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
        IsOwnerOfSim
    )
    http_method_names = ('get', 'post')

    def get_queryset(self):
        return CallHistory.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CallHistoryCreateSerializer
        return self.serializer_class
