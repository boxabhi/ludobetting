from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Game)
admin.site.register(GameResult)
admin.site.register(Image)


class DisputedGameAdmin(admin.ModelAdmin):
    list_display = ('game' , 'is_reviewed', 'game_amount' , 'game_creater_by' , 'created_at')
    
    def game_amount(self, obj):
        return obj.game.coins
    
    def game_creater_by(self, obj):
        return obj.game.game_creater
    
    def created_at(self,obj):
        return obj.game.created_at


admin.site.register(DisputedGame , DisputedGameAdmin)
