from django.contrib import admin

from .models import Phone, Sim, CallHistory, ChargingHistory, BalanceHistory, SMS, PowerSocket

admin.site.register(Phone)
admin.site.register(Sim)
admin.site.register(CallHistory)
admin.site.register(ChargingHistory)
admin.site.register(BalanceHistory)
admin.site.register(SMS)
admin.site.register(PowerSocket)
