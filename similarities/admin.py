from django.contrib import admin

from .models import GeneralArtist, Similarity


class SimilarityModelAdmin(admin.ModelAdmin):
    fields = ['other_artist', 'cc_artist', 'weight']
    list_display = ['id', 'other_artist', 'cc_artist', 'weight']
    readonly_fields = ['other_artist', 'cc_artist']


admin.site.register(GeneralArtist)
admin.site.register(Similarity, SimilarityModelAdmin)
