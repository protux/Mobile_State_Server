from django.urls import path

from mosta.dashboard.views import DashBoardView

app_name = 'dashboard'
urlpatterns = [
    path('', DashBoardView.as_view(), name='dashboard'),
]
