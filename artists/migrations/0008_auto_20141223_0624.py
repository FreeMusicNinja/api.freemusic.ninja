# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0007_auto_20140923_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fmaartist',
            name='artist_images',
            field=jsonfield.fields.JSONField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fmaartist',
            name='tags',
            field=jsonfield.fields.JSONField(null=True),
            preserve_default=True,
        ),
    ]
