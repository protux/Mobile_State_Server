from django.views.generic import TemplateView, RedirectView
from django.urls import reverse_lazy


class HomepageView(TemplateView):
    template_name = 'pages/homepage.html'


class RedirectHomepageOrDashboardView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('dashboard:dashboard')
        else:
            return reverse_lazy('pages:homepage')
