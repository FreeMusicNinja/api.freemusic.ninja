from django.db import models
from model_utils.models import TimeStampedModel


class Artist(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    url = models.URLField(max_length=2000)
    website = models.URLField(null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Album(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    url = models.URLField(max_length=2000)
    artist = models.ForeignKey(Artist, null=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Track(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=2000)
    image_file = models.URLField(max_length=2000, null=True)
    artist = models.ForeignKey(Artist, null=True)
    album = models.ForeignKey(Album, null=True)
    license_title = models.CharField(max_length=255, null=True)
    license_url = models.URLField(max_length=2000, null=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title
