# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_artists(apps, schema_editor):
    Artist = apps.get_model("fma", "Artist")
    db_alias = schema_editor.connection.alias
    for artist in Artist.objects.using(db_alias).all():
        artist.save(using=db_alias)


class Migration(migrations.Migration):

    dependencies = [
        ('fma', '0002_auto_20150105_0651'),
    ]

    operations = [
        migrations.RunPython(
            update_artists,
        ),
    ]
