from allauth.account.decorators import verified_email_required
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from mosta.base.utils import message_utils
from mosta.phone.models import Phone, Sim


@method_decorator(verified_email_required, name='dispatch')
class ListPhonesView(ListView):
    context_object_name = 'phones'

    def get_queryset(self):
        return Phone.objects.filter(owner=self.request.user)


@method_decorator(verified_email_required, name='dispatch')
class DisplayPhoneView(DetailView):
    context_object_name = 'phone'

    def get_object(self, queryset=None):
        phone = super().get_object(queryset=queryset)
        sims = Sim.objects.filter(phone=phone)
        if len(sims) > 0:
            phone.sims = sims
        return phone

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Phone.objects.filter(pk=pk, owner=self.request.user)


@method_decorator(verified_email_required, name='dispatch')
class CreatePhoneView(CreateView):
    model = Phone
    fields = ('label',)

    def __init__(self):
        super().__init__()
        self.object = None

    def get_success_url(self):
        return reverse_lazy('phone:display_phone', args=[self.object.id])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        try:
            self.object.save()
        except IntegrityError:
            message_utils.add_error_message(self.request.session, _('You already have a phone with this label.'))
            return HttpResponseRedirect(reverse_lazy('phone:create_phone'))
        return super(ModelFormMixin, self).form_valid(form)


@method_decorator(verified_email_required, name='dispatch')
class UpdatePhoneView(UpdateView):
    model = Phone
    fields = ('label', 'attached_power_socket')

    def get_success_url(self):
        return reverse_lazy('phone:display_phone', args=[self.object.id])

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Phone.objects.filter(pk=pk, owner=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            message_utils.add_error_message(self.request.session, _('You already have a phone with this label.'))
            return HttpResponseRedirect(reverse_lazy('phone:update_phone', args=[self.kwargs.get(self.pk_url_kwarg)]))


@method_decorator(verified_email_required, name='dispatch')
class DeletePhoneView(DeleteView):
    model = Phone
    success_url = reverse_lazy('phone:list_phones')
    context_object_name = 'phone'

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Phone.objects.filter(pk=pk, owner=self.request.user)
