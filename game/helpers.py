from .models import *
from accounts.models import *
from transaction.models import *







def game_cron_job():
    games_obj = Game.objects.filter(status='RUNNING')
    for game in games_obj:
        game_result_obj = GameResult.objects.filter(game = game)
        
        if len(game_result_obj) >= 2:
            
            game_result_obj_one = game_result_obj[0]
            game_result_obj_two = game_result_obj[1]
            
            print(game_result_obj_one.result)
            print(game_result_obj_two.result)
            
            winning_amount = 0
            
            if game.coins < 250:
                winning_amount = .90 * game.coins
            elif game.coins >= 250 and game.coins <500:
                winning_amount =  game.coins - 25
            else:
                winning_amount = .95 * game.coins
                
                
                
                
            
            
            if game_result_obj_one.result != 'PENDING' and game_result_obj_two.result != 'PENDING':
                if game_result_obj_one.result == 'WON' and game_result_obj_two.result == 'LOST':
                    winner = Profile.objects.filter(user = game_result_obj_one.user).first()
                    winner.coins +=  winning_amount
                    game_result_obj_one.winning_amount =  winning_amount
                    game_result_obj_one.result  = 'WON'
                    game_result_obj_one.save()
                    winner.save()
                    
                elif game_result_obj_one.result == 'LOST' and game_result_obj_two.result == 'WON':
                    winner = Profile.objects.filter(user = game_result_obj_two.user).first()
                    winner.coins += winning_amount
                    game_result_obj_two.winning_amount =  winning_amount
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
                
                elif game_result_obj_one.result == 'LOST' and game_result_obj_one.result == 'LOST':
                    user_obj_one = Profile.objects.filter(user = game_result_obj_one.user).first()
                    user_obj_two = Profile.objects.filter(user = game_result_obj_two.user).first()
                    user_obj_one.coins += game.coins
                    user_obj_two.coins += game.coins
                    game_result_obj_two.result  = 'CANCEL'
                    game_result_obj_one.result  = 'CANCEL'
                    game_result_obj_two.save()
                    game_result_obj_one.save()
                    
                    user_obj_one.save()
                    user_obj_two.save()
                    
                    penalty_obj_one = Penalty(user =user_obj_one.user , amount = 25 , reason='You both updated Lost')
                    penalty_obj_two = Penalty(user =user_obj_two.user , amount = 25 , reason='You both updated Lost') 
                    penalty_obj_one.save()
                    penalty_obj_two.save() 
                     
                game.status = 'OVER'
                game.save()    
                    
                
                
            
        
        
        
    