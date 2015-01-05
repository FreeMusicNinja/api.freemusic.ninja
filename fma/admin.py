from django.contrib import admin

from . import models, queries


def query_from_api(modeladmin, request, queryset):
    for artist in queryset:
        try:
            queries.query_tracks(artist)
        except queries.FMAQueryException:
            pass  # ignore these for the admin command
        else:
            artist.save()


class SignificantAlbumListFilter(admin.SimpleListFilter):
    title = "Select with significant albums"
    parameter_name = 'tracks_in_album'

    def lookups(self, request, model_admin):
        return (
            ('2', "more than 1"),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        albums = models.Album.objects.annotate(models.models.Count('track')).filter(track__count__gte=self.value())
        return queryset.filter(album__in=albums).distinct()


class AlbumInline(admin.TabularInline):
    model = models.Album


class TrackInline(admin.TabularInline):
    model = models.Track


admin.site.register(models.Artist, actions=(query_from_api,), list_filter=(SignificantAlbumListFilter,))
admin.site.register(models.Album)
admin.site.register(models.Track)
admin.site.register(models.Genre)
