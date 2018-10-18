from django.urls import path

from .views.phone import ListPhonesView, DisplayPhoneView, UpdatePhoneView, CreatePhoneView, DeletePhoneView
from .views.power_socket import ListPowerSocketsView, DisplayPowerSocketView, CreatePowerSocketView, \
    UpdatePowerSocketView, DeletePowerSocketView
from .views.sim import ListSimsView, DisplaySimView, CreateSimView, UpdateSimView, DeleteSimView

app_name = 'phone'
urlpatterns = [
    path('phone/', ListPhonesView.as_view(), name='list_phones'),
    path('phone/<int:pk>/', DisplayPhoneView.as_view(), name='display_phone'),
    path('phone/<int:pk>/edit/', UpdatePhoneView.as_view(), name='update_phone'),
    path('phone/<int:pk>/delete/', DeletePhoneView.as_view(), name='delete_phone'),
    path('phone/add/', CreatePhoneView.as_view(), name='create_phone'),

    path('sim/', ListSimsView.as_view(), name='list_sims'),
    path('sim/<int:pk>/', DisplaySimView.as_view(), name='display_sim'),
    path('sim/<int:pk>/edit/', UpdateSimView.as_view(), name='update_sim'),
    path('sim/<int:pk>/delete/', DeleteSimView.as_view(), name='delete_sim'),
    path('sim/add/', CreateSimView.as_view(), name='create_sim'),

    path('powersocket/', ListPowerSocketsView.as_view(), name='list_power_sockets'),
    path('powersocket/<int:pk>/', DisplayPowerSocketView.as_view(), name='display_power_socket'),
    path('powersocket/<int:pk>/edit/', UpdatePowerSocketView.as_view(), name='update_power_socket'),
    path('powersocket/<int:pk>/delete/', DeletePowerSocketView.as_view(), name='delete_power_socket'),
    path('powersocket/add/', CreatePowerSocketView.as_view(), name='create_power_socket'),
]
