from django.conf import settings as django_settings
from django.db import models

from mosta.base.validators import positive_number


class PowerSocket(models.Model):
    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=25)
    namespace = models.CharField(max_length=10)
    socket_id = models.IntegerField(validators=[positive_number])
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{} ({} - {})'.format(self.label, self.namespace, self.socket_id)

    class Meta:
        unique_together = (('namespace', 'socket_id'), ('owner', 'label'),)
