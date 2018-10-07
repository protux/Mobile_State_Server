from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwner, IsOwnerOfSim
from mosta.api.serializers.sms import SMSCreateSerializer, SMSSerializer
from mosta.phone.models import SMS


class SMSViewSet(viewsets.ModelViewSet):
    queryset = SMS.objects.all()
    serializer_class = SMSSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
        IsOwnerOfSim
    )
    http_method_names = ('get', 'post')

    def get_queryset(self):
        return SMS.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SMSCreateSerializer
        return self.serializer_class
