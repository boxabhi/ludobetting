from django.contrib import admin
from .models import *
# Register your models here.
from django.template.response import TemplateResponse


admin.site.register(Game)
admin.site.register(GameResult)



class ImagesAdmin(admin.ModelAdmin):
    fields = ('user','photo_tag',  'game_result')
    readonly_fields = ('user','photo_tag','game_result')
    
    # def photo_tag(self):
    #     return mark_safe('<a href="/media/{0}"><img src="/media/{0}"></a>'.format(self.uploaded_image))
   


admin.site.register(Image , ImagesAdmin)

from django.utils.safestring import mark_safe





class DisputedGameAdmin(admin.ModelAdmin):
    list_display = ('game' , 'is_reviewed', 'game_played_between' , 'game_creater_by' , 'created_at')
    readonly_fields = ('game_played_between','images')
    list_filter =( 'is_reviewed' , 'created_at')
    
    def game_amount(self, obj):
        return obj.game.coins
    
    def game_creater_by(self, obj):
        return obj.game.game_creater
    
    def game_played_between(self, obj):
        game_obj = obj.game
        game_players = ''
        try:
            player_one = User.objects.get(id = game_obj.player_one)
            player_two = User.objects.get(id = game_obj.player_two)
            game_players += (player_one.username).upper() + ' VS ' + (player_two.username).upper()
        except Exception as e:
            pass
        return mark_safe(f'<h1 style="font-weight:bold">{game_players} </h1>')
    
    def created_at(self,obj):
        return obj.game.created_at
    
    def images(self, obj):
        im= Image.objects.filter(game = obj.game)
        temp = ''
        for i in im:
            print(i.user.username)
            temp += (f'<h4 style="margin-top:12px">{(i.user.username).upper()}</h4><img src="/media/{i.uploaded_image}" style="height:300px; width:300px>')
            temp += '<div style="margin-top:15px;padding-left:1000px !important"></div>'
        print(temp)    
        return mark_safe(temp)

admin.site.register(DisputedGame , DisputedGameAdmin)
