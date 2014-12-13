from django.contrib import admin

from . import models

admin.site.register(
    models.Artist,
    list_display=('name', 'location'),
)

admin.site.register(
    models.Album,
    list_display=('title', 'license'),
    list_filter=('license',),
    readonly_fields=('artist',),
)
