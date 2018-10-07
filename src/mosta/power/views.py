from allauth.account.decorators import verified_email_required
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from mosta.base.utils import message_utils
from .models import PowerSocket


@method_decorator(verified_email_required, name='dispatch')
class ListPowerSocketsView(ListView):
    context_object_name = 'power_sockets'

    def get_queryset(self):
        return PowerSocket.objects.filter(owner=self.request.user)


@method_decorator(verified_email_required, name='dispatch')
class DisplayPowerSocketView(DetailView):
    context_object_name = 'power_socket'

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return PowerSocket.objects.filter(pk=pk, owner=self.request.user)


@method_decorator(verified_email_required, name='dispatch')
class CreatePowerSocketView(CreateView):
    model = PowerSocket
    fields = ('label', 'namespace', 'socket_id')

    def __init__(self):
        super().__init__()
        self.object = None

    def get_success_url(self):
        return reverse_lazy('power:display', args=[self.object.id])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        try:
            self.object.save()
        except IntegrityError:
            message_utils.add_error_message(
                self.request.session,
                _('You already created a power socket with this parameters.')
            )
            return HttpResponseRedirect(reverse_lazy('power:create'))
        return super(ModelFormMixin, self).form_valid(form)


@method_decorator(verified_email_required, name='dispatch')
class UpdatePowerSocketView(UpdateView):
    model = PowerSocket
    fields = ('label', 'namespace', 'socket_id')

    def get_success_url(self):
        return reverse_lazy('power:display', args=[self.object.id])

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return PowerSocket.objects.filter(pk=pk, owner=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            message_utils.add_error_message(
                self.request.session,
                _('You already created a power socket with this parameters.')
            )
            return HttpResponseRedirect(reverse_lazy('power:update', args=[self.kwargs.get(self.pk_url_kwarg)]))


@method_decorator(verified_email_required, name='dispatch')
class DeletePowerSocketView(DeleteView):
    model = PowerSocket
    success_url = reverse_lazy('power:list')
    context_object_name = 'power_socket'

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return PowerSocket.objects.filter(pk=pk, owner=self.request.user)
