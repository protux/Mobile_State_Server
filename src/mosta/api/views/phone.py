from rest_framework import permissions, viewsets

from mosta.api.permissions import IsOwner
from mosta.api.serializers.phone import PhoneSerializer
from mosta.phone.models import Phone


class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner
    )
    http_method_names = ('get', 'post', 'put')

    def get_queryset(self):
        return Phone.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
