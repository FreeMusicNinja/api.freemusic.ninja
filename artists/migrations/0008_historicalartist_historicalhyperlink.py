# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artists', '0007_auto_20140923_0804'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalArtist',
            fields=[
                ('id', models.IntegerField(db_index=True, auto_created=True, verbose_name='ID', blank=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'historical artist',
                'ordering': ('-history_date', '-history_id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalHyperlink',
            fields=[
                ('id', models.IntegerField(db_index=True, auto_created=True, verbose_name='ID', blank=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('order', models.IntegerField()),
                ('artist_id', models.IntegerField(db_index=True, blank=True, null=True)),
                ('name', models.CharField(choices=[('bandcamp', 'Bandcamp'), ('jamendo', 'Jamendo'), ('magnatune', 'Magnatune'), ('fma', 'Free Music Archive'), ('homepage', 'Homepage')], max_length=50)),
                ('url', models.URLField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'historical hyperlink',
                'ordering': ('-history_date', '-history_id'),
            },
            bases=(models.Model,),
        ),
    ]
