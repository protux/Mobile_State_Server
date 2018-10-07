from allauth.account.decorators import verified_email_required
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from mosta.base.utils import message_utils
from mosta.phone.models import Sim


@method_decorator(verified_email_required, name='dispatch')
class ListSimsView(ListView):
    context_object_name = 'sims'

    def get_queryset(self):
        return Sim.objects.filter(owner=self.request.user)


@method_decorator(verified_email_required, name='dispatch')
class DisplaySimView(DetailView):
    context_object_name = 'sim'

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Sim.objects.filter(pk=pk, owner=self.request.user)


@method_decorator(verified_email_required, name='dispatch')
class CreateSimView(CreateView):
    model = Sim
    fields = ('phone', 'label', 'phone_number', 'can_call',)

    def __init__(self):
        super().__init__()
        self.object = None

    def get_success_url(self):
        return reverse_lazy('phone:display_sim', args=[self.object.id])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        try:
            self.object.save()
        except IntegrityError:
            message_utils.add_error_message(self.request.session, _('You already have a sim with this label.'))
            return HttpResponseRedirect(reverse_lazy('phone:create_sim'))
        return super(ModelFormMixin, self).form_valid(form)


@method_decorator(verified_email_required, name='dispatch')
class UpdateSimView(UpdateView):
    model = Sim
    fields = ('phone', 'label', 'phone_number', 'can_call',)

    def get_success_url(self):
        return reverse_lazy('phone:display_sim', args=[self.object.id])

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Sim.objects.filter(pk=pk, owner=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            message_utils.add_error_message(self.request.session, _('You already have a sim with this label.'))
            return HttpResponseRedirect(reverse_lazy('phone:update_sim', args=[self.kwargs.get(self.pk_url_kwarg)]))


@method_decorator(verified_email_required, name='dispatch')
class DeleteSimView(DeleteView):
    model = Sim
    success_url = reverse_lazy('phone:list_sims')
    context_object_name = 'sim'

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Sim.objects.filter(pk=pk, owner=self.request.user)
