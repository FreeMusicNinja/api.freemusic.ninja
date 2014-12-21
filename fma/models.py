from django.db import models
import jsonfield
from model_utils.models import TimeStampedModel


class Artist(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    handle = models.CharField(max_length=250, null=True)
    url = models.URLField(max_length=2000)
    name = models.CharField(max_length=250)
    bio = models.CharField(max_length=50000, null=True)
    members = models.CharField(max_length=15000, null=True)
    website = models.URLField(null=True)
    wikipedia_page = models.URLField(null=True)
    donation_url = models.URLField(null=True)
    contact = models.CharField(max_length=200, null=True)
    active_year_begin = models.CharField(max_length=4, null=True)
    active_year_end = models.CharField(max_length=4, null=True)
    related_projects = models.CharField(max_length=2000, null=True)
    associated_labels = models.CharField(max_length=500, null=True)
    comments = models.IntegerField(null=True)
    favorites = models.IntegerField(null=True)
    date_created = models.DateTimeField(null=True)
    flattr_name = models.CharField(max_length=100, null=True)
    paypal_name = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)
    image_file = models.URLField(null=True)
    location = models.CharField(max_length=500, null=True)
    tags = jsonfield.JSONField(null=True)
    images = jsonfield.JSONField(null=True)

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
