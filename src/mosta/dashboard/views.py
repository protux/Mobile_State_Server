from allauth.account.decorators import verified_email_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .utils import dashboard_utils


@method_decorator(verified_email_required, name='dispatch')
class DashBoardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'missing_phones': dashboard_utils.get_missing_phones(self.request.user),
            'latest_sms': dashboard_utils.get_latest_sms(self.request.user),
            'average_call_divergences_per_sim': dashboard_utils.get_sim_cards_divergent_from_average_call_duration(
                self.request.user, 10, timezone.now()
            ),
            'charging_phones': dashboard_utils.get_phones_charging(self.request.user),
            'phones_requiring_energy': dashboard_utils.get_phones_requiring_energy(self.request.user),
            'call_duration_data_set': dashboard_utils.get_call_duration_over_time_per_sim(self.request.user)
        })
        return context
