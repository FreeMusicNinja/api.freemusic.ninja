# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_missing_know_artists(apps, schema_editor):
    User = apps.get_model("users", "User")
    KnownArtist = apps.get_model("similarities", "KnownArtist")
    GeneralArtist = apps.get_model("similarities", "GeneralArtist")
    for user in User.objects.all():
        for sim in user.usersimilarity_set.all():
            cc_artists = GeneralArtist.objects.filter(
                normalized_name=sim.cc_artist.name.upper())
            KnownArtist.objects.get_or_create(artist=sim.other_artist,
                                              user=user)
            for artist in cc_artists:
                KnownArtist.objects.get_or_create(artist=artist, user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('similarities', '0004_auto_20150118_0900'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_missing_know_artists),
    ]
