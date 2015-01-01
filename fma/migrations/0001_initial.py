# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250, null=True)),
                ('url', models.URLField(max_length=2000)),
            ],
            options={
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('handle', models.CharField(max_length=250, null=True)),
                ('url', models.URLField(max_length=2000)),
                ('name', models.CharField(max_length=250)),
                ('bio', models.CharField(max_length=50000, null=True)),
                ('members', models.CharField(max_length=15000, null=True)),
                ('website', models.URLField(null=True)),
                ('wikipedia_page', models.URLField(null=True)),
                ('donation_url', models.URLField(null=True)),
                ('contact', models.CharField(max_length=200, null=True)),
                ('active_year_begin', models.CharField(max_length=4, null=True)),
                ('active_year_end', models.CharField(max_length=4, null=True)),
                ('related_projects', models.CharField(max_length=2000, null=True)),
                ('associated_labels', models.CharField(max_length=500, null=True)),
                ('comments', models.IntegerField(null=True)),
                ('favorites', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('flattr_name', models.CharField(max_length=100, null=True)),
                ('paypal_name', models.CharField(max_length=100, null=True)),
                ('latitude', models.CharField(max_length=20, null=True)),
                ('longitude', models.CharField(max_length=20, null=True)),
                ('image_file', models.URLField(null=True)),
                ('location', models.CharField(max_length=500, null=True)),
                ('tags', jsonfield.fields.JSONField(null=True)),
                ('images', jsonfield.fields.JSONField(null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField(max_length=2000)),
                ('image_file', models.URLField(max_length=2000, null=True)),
                ('license_title', models.CharField(max_length=250, null=True)),
                ('license_url', models.URLField(max_length=2000, null=True)),
                ('language_code', models.CharField(max_length=100, null=True)),
                ('duration', models.CharField(max_length=100, null=True)),
                ('number', models.IntegerField(null=True)),
                ('disc_number', models.IntegerField(null=True)),
                ('explicit', models.CharField(max_length=100, null=True)),
                ('explicit_notes', models.TextField(null=True)),
                ('copyright_c', models.CharField(max_length=200, null=True)),
                ('copyright_p', models.CharField(max_length=200, null=True)),
                ('composer', models.CharField(max_length=250, null=True)),
                ('lyricist', models.CharField(max_length=250, null=True)),
                ('publisher', models.CharField(max_length=250, null=True)),
                ('instrumental', models.NullBooleanField()),
                ('information', models.CharField(max_length=250, null=True)),
                ('date_recorded', models.DateField(null=True)),
                ('comments', models.IntegerField(null=True)),
                ('favorites', models.IntegerField(null=True)),
                ('listens', models.IntegerField(null=True)),
                ('interest', models.IntegerField(null=True)),
                ('bit_rate', models.IntegerField(null=True)),
                ('date_created', models.CharField(max_length=100, null=True)),
                ('file', models.CharField(max_length=250, null=True)),
                ('license_image_file', models.URLField(max_length=2000, null=True)),
                ('license_image_file_large', models.URLField(max_length=2000, null=True)),
                ('license_parent_id', models.IntegerField(null=True)),
                ('tags', jsonfield.fields.JSONField(null=True)),
                ('album', models.ForeignKey(null=True, to='fma.Album')),
                ('artist', models.ForeignKey(null=True, to='fma.Artist')),
                ('genres', models.ManyToManyField(to='fma.Genre')),
            ],
            options={
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, to='fma.Artist'),
            preserve_default=True,
        ),
    ]
