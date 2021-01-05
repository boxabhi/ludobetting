from django.contrib import admin
from .models import *
# Register your models here.


class OrderCoinsAdmin(admin.ModelAdmin):
    list_display = ('user' , 'amount' , 'order_id' , 'status' , 'created_at') 

admin.site.register(OrderCoins , OrderCoinsAdmin)

class SellCoinsAdmin(admin.ModelAdmin):
    list_display = ('user' , 'amount' , 'payment_mode' , 'number' , 'is_paid' ,'created_at') 

admin.site.register(SellCoins , SellCoinsAdmin)

class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('user' , 'amount' , 'reason' , 'created_at')


admin.site.register(Penalty,PenaltyAdmin)
admin.site.register(CashFree)
admin.site.register(ReffralBonous)