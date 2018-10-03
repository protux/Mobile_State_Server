from rest_framework import permissions, viewsets

from mosta.phone.models import Phone
from mosta.api.permissions import IsOwner
from mosta.api.serializers.phone import PhoneSerializer


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
        serializer.save(owner=self.request.user)

