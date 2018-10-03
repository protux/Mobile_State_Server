from django.conf.urls import url
from django.urls import path

from .views import ListPhonesView, DisplayPhoneView, UpdatePhoneView, CreatePhoneView, DeletePhoneView

app_name = 'phone'
urlpatterns = [
    url(r'^$', ListPhonesView.as_view(), name='list'),
    path('<int:pk>/', DisplayPhoneView.as_view(), name='display'),
    path('<int:pk>/edit/', UpdatePhoneView.as_view(), name='update'),
    path('<int:pk>/delete/', DeletePhoneView.as_view(), name='delete'),
    url('add/', CreatePhoneView.as_view(), name='create'),
]
