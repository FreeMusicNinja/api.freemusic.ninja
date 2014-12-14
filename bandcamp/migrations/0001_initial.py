# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(null=True, max_length=255)),
                ('url', models.URLField(unique=True)),
                ('art', models.URLField(null=True)),
                ('release_date', models.CharField(null=True, max_length=100)),
                ('license', models.CharField(null=True, blank=True, max_length=255)),
                ('as_of', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(null=True, max_length=255)),
                ('url', models.URLField(unique=True)),
                ('location', models.CharField(null=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, to='bandcamp.Artist'),
            preserve_default=True,
        ),
    ]
