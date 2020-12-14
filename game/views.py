from django.shortcuts import render

# Create your views here.



def game_playing(request):
    return render(request, 'game/game_playing.html')