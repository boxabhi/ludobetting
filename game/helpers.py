from .models import *
from accounts.models import *








def game_cron_job():
    games_obj = Game.objects.filter(status='RUNNING')
    print(games_obj)
    for game in games_obj:
        game_result_obj = GameResult.objects.filter(game = game)
        
        if len(game_result_obj) >= 2:
            
            game_result_obj_one = game_result_obj[0]
            game_result_obj_two = game_result_obj[1]
            
            
            
            if game_result_obj_one != 'PENDING' and game_result_obj_two != 'PENDING':
                if game_result_obj_one.result == 'WON' and game_result_obj_two.result == 'LOST':
                    winner = Profile.objects.filter(user = game_result_obj_one.user).first()
                    winner.coins +=  (.95 * game.coins) + game.coins
                    game_result_obj_one.result  = 'WON'
                    game_result_obj_one.save()
                    winner.save()
                    
                elif game_result_obj_one.result == 'LOST' and game_result_obj_two.result == 'WON':
                    winner = Profile.objects.filter(user = game_result_obj_two.user).first()
                    winner.coins +=  (.95 * game.coins) + game.coins
                    game_result_obj_two.result  = 'WON'
                    game_result_obj_two.save()
                    winner.save()
                elif game_result_obj_one.result == 'CANCEL' and game_result_obj_one.result == 'CANCEL':
                    user_obj_one = Profile.objects.filter(user = game_result_obj_one.user).first()
                    user_obj_two = Profile.objects.filter(user = game_result_obj_two.user).first()
                    user_obj_one.coins += game.coins
                    user_obj_two.coins += game.coins
                    user_obj_one.save()
                    user_obj_two.save()
                   
                    game_result_obj_two.result  = 'CANCEL'
                    game_result_obj_one.result  = 'CANCEL'
                    game_result_obj_two.save()
                    game_result_obj_one.save()
                elif game_result_obj_one.result == 'WON' and game_result_obj_two.result == 'WON':
                    disputed = DisputedGame(game = game)
                    disputed.save()
                
                game.status = 'OVER'
                game.save()    
                    
                
                
            
        
        
        
    