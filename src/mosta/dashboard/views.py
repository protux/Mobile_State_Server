from allauth.account.decorators import verified_email_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .utils import dashboard_utils


# TODO average balance per day over time (last seven days)
# TODO average call time per day over seven days
# TODO show phones with less than n calls on specific date
# TODO show average battery lifetime

@method_decorator(verified_email_required, name='dispatch')
class DashBoardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'missing_phones': dashboard_utils.get_missing_phones(self.request.user),
            'latest_sms': dashboard_utils.get_latest_sms(self.request.user),
        })
        return context
