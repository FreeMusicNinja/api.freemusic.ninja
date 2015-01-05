# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0008_auto_20141223_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='hyperlink',
            name='num_tracks',
            field=models.IntegerField(null=True, default=None, blank=True),
            preserve_default=True,
        ),
    ]
