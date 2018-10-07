from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwner
from mosta.api.serializers.sim import SimSerializer
from mosta.phone.models import Sim


class SimViewSet(viewsets.ModelViewSet):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner
    )
    http_method_names = ('get', 'post', 'put')

    def get_queryset(self):
        return Sim.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
