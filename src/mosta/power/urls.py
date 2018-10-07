from django.conf.urls import url
from django.urls import path

from .views import ListPowerSocketsView, DisplayPowerSocketView, CreatePowerSocketView, UpdatePowerSocketView, \
    DeletePowerSocketView

app_name = 'power'
urlpatterns = [
    url(r'^$', ListPowerSocketsView.as_view(), name='list'),
    path('<int:pk>/', DisplayPowerSocketView.as_view(), name='display'),
    path('<int:pk>/edit/', UpdatePowerSocketView.as_view(), name='update'),
    path('<int:pk>/delete/', DeletePowerSocketView.as_view(), name='delete'),
    url('add/', CreatePowerSocketView.as_view(), name='create'),
]
