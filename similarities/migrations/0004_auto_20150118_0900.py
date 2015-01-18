# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('similarities', '0003_auto_20141028_0416'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnownArtist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('artist', models.ForeignKey(to='similarities.GeneralArtist')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='knownartist',
            unique_together=set([('artist', 'user')]),
        ),
        migrations.AddField(
            model_name='generalartist',
            name='known_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='similarities.KnownArtist', related_name='known_artists'),
            preserve_default=True,
        ),
    ]
