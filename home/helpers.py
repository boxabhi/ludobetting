from accounts.models import *


def set_coins(request):
    profile = Profile.objects.filter(user=request.user).first()
    request.session['coins'] = profile.coins