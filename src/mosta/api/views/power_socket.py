from rest_framework import permissions, viewsets

from mosta.phone.utils import power_socket_utils
from mosta.phone.models import PowerSocket
from mosta.api.serializers.power_socket import PowerSocketSerializer
from mosta.api.permissions import IsOwner


class PowerSocketViewSet(viewsets.ModelViewSet):
    queryset = PowerSocket.objects.all()
    serializer_class = PowerSocketSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner
    )
    http_method_names = ('get', 'post', 'put')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data['activation_required'] = power_socket_utils.needs_power_socket_activation(response.data['id'])
        return response

    def get_queryset(self):
        return PowerSocket.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
