from django.contrib import admin
from .models import *
# Register your models here.


class OrderCoinRequestAdmin(admin.ModelAdmin):
    list_display = ('amount' , 'order_id' , 'is_approved' , 'user' , 'created_at')
    list_filter =( 'user' ,'amount','is_approved', 'created_at')
    list_per_page = 20
    
admin.site.register(OrderCoinRequest , OrderCoinRequestAdmin)    


class PaytmOrderIdAdmin(admin.ModelAdmin):
    list_display = ('amount' , 'order_id' , 'is_used' , 'used_by' , 'created')
    list_filter =( 'used_by' ,'amount','is_used', 'created')
    list_per_page = 20
    
admin.site.register(PaytmOrderId , PaytmOrderIdAdmin)    

class OrderCoinsAdmin(admin.ModelAdmin):
    list_display = ('user' , 'amount' , 'order_id' , 'status' , 'created_at') 
    list_filter =( 'user' ,'amount','status', 'created_at')
    list_per_page = 20

admin.site.register(OrderCoins , OrderCoinsAdmin)

class SellCoinsAdmin(admin.ModelAdmin):
    list_display = ('user','user_register_number' , 'amount' , 'payment_mode' , 'number', 'is_paid' ,'created_at') 
    list_filter =( 'user','amount' , 'is_paid','payment_mode' , 'created_at')
    search_fields = ('user' , 'amount', 'payment_mode')
    list_per_page = 20
    
admin.site.register(SellCoins , SellCoinsAdmin)

class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('user' , 'amount' , 'reason' , 'created_at')


admin.site.register(Penalty,PenaltyAdmin)
admin.site.register(CashFree)
admin.site.register(ReffralBonous)