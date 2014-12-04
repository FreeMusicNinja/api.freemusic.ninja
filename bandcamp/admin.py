from django.contrib import admin

from . import models

admin.site.register(
    models.Album,
    list_display=('title', 'license'),
    list_filter=('license',),
)
