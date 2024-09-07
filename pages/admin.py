from django.contrib import admin

from pages.models import Favorite


# Register your models here.
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass