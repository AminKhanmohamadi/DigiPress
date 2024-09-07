from .models import Favorite

def len_favorites(request):
    if request.user.is_authenticated:
        favorites_count = Favorite.objects.filter(user=request.user).count()
    else:
        favorites_count = 0

    return {'favorites_count': favorites_count}
