from django.contrib import admin

from fma.admin import query_from_api

from .models import Artist, JamendoArtist, MagnatuneArtist, FMAArtist


class ArtistModelAdmin(admin.ModelAdmin):
    search_fields = ['name']


class JamendoArtistModelAdmin(admin.ModelAdmin):
    search_fields = ['name']


class MagnatuneArtistModelAdmin(admin.ModelAdmin):
    search_fields = ['artist']


class FMAArtistModelAdmin(admin.ModelAdmin):
    search_fields = ['artist_name']


admin.site.register(Artist, ArtistModelAdmin)
admin.site.register(JamendoArtist, JamendoArtistModelAdmin)
admin.site.register(MagnatuneArtist, MagnatuneArtistModelAdmin)
admin.site.register(FMAArtist, FMAArtistModelAdmin, actions=(query_from_api,))
