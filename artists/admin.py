from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Artist, JamendoArtist, MagnatuneArtist


admin.site.register(Artist, SimpleHistoryAdmin)
admin.site.register(JamendoArtist)
admin.site.register(MagnatuneArtist)
