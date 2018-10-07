from django.conf.urls import url

from .views import HomepageView

app_name = 'pages'
urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='homepage'),
]
