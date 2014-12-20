from django.contrib import admin

from fma.admin import query_from_api

from .models import Artist, JamendoArtist, MagnatuneArtist, FMAArtist


admin.site.register(Artist)
admin.site.register(JamendoArtist)
admin.site.register(MagnatuneArtist)
admin.site.register(FMAArtist, actions=(query_from_api,))
