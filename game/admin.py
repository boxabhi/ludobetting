from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Game)
admin.site.register(GameResult)



class ImagesAdmin(admin.ModelAdmin):
    fields = ('user','photo_tag',  'game_result')
    readonly_fields = ('user','photo_tag','game_result')
    
    # def photo_tag(self):
    #     return mark_safe('<a href="/media/{0}"><img src="/media/{0}"></a>'.format(self.uploaded_image))
   


admin.site.register(Image , ImagesAdmin)




class DisputedGameAdmin(admin.ModelAdmin):
    list_display = ('game' , 'is_reviewed', 'game_amount' , 'game_creater_by','image' , 'created_at')
    
    def game_amount(self, obj):
        return obj.game.coins
    
    def game_creater_by(self, obj):
        return obj.game.game_creater
    
    def created_at(self,obj):
        return obj.game.created_at
    
    def images(self, obj):
        im= DisputedGame.objects.get(game = obj.game)
        print(disputed_game)
        return self.disputed_game

admin.site.register(DisputedGame , DisputedGameAdmin)
