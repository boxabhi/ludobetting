from django.contrib import admin
from .models import *
# Register your models here.
from django.template.response import TemplateResponse
from django import forms
from django.db.models import Q

admin.site.register(Game)
admin.site.register(GameResult)



class ImagesAdmin(admin.ModelAdmin):
    fields = ('user','photo_tag',  'game_result')
    readonly_fields = ('user','photo_tag','game_result')
    
    # def photo_tag(self):
    #     return mark_safe('<a href="/media/{0}"><img src="/media/{0}"></a>'.format(self.uploaded_image))
   


admin.site.register(Image , ImagesAdmin)

from django.utils.safestring import mark_safe


class CategoryChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "{}".format((obj.username).upper())



class DisputedGameAdmin(admin.ModelAdmin):
    list_display = ('game' , 'is_reviewed', 'game_played_between' , 'game_creater_by' , 'created_at')
    readonly_fields = ('result_updated','room_code','game_played_between','images'  )
    list_filter =( 'is_reviewed' , 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'winner':
            disputed_game_obj = DisputedGame.objects.get(id = int(request.META['PATH_INFO'].rstrip('/').split('/')[4]))
            game_obj = Game.objects.get(id = disputed_game_obj.game.id)
            player_one = User.objects.get(id = game_obj.player_one)
            player_two = User.objects.get(id = game_obj.player_two)
            
            return CategoryChoiceField(queryset=User.objects.filter(Q(id =game_obj.player_one) | Q(id = game_obj.player_two)))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def game_amount(self, obj):
        return obj.game.coins
    
    def room_code(self, obj):
        return mark_safe(f'<h2>{obj.game.room_code}</h2>')
        
    
    
    def game_creater_by(self, obj):
        return obj.game.game_creater
    
    def get_users(self):
        print(self)
        try:
            player_one = User.objects.get(id = game_obj.player_one)
            player_two = User.objects.get(id = game_obj.player_two)
            user_list = []
            user_list.append(player_one)
            user_list.append(player_two)
            print(user_list)
            return user_list
        except Exception as e:
            print(e)
            
    
    def result_updated(self , obj):
        game_results = GameResult.objects.filter(game = obj.game)
        html = ''
        for g in game_results:
            html += f'<p> <b>{(g.user.username).upper()}</b> updated - {g.result_updated}</p>'
        return mark_safe(html)
            
    
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
