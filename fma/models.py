from django.db import models
import jsonfield
from model_utils.models import TimeStampedModel

from artists import models as artists_models


class Genre(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    url = models.URLField()

    def __str__(self):
        return self.title


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # crude updating of known artists and hyperlinks
        artist, _ = artists_models.Artist.objects.get_or_create(name=self.name)
        artists_models.Hyperlink.objects.get_or_create(
            artist=artist,
            name='fma',
            defaults={'order': 40, 'url': self.url},
        )

    def __str__(self):
        return self.name


class Album(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250, null=True)
    url = models.URLField(max_length=2000)
    artist = models.ForeignKey(Artist, null=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Track(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=2000)
    image_file = models.URLField(max_length=2000, null=True)
    artist = models.ForeignKey(Artist, null=True)
    album = models.ForeignKey(Album, null=True)
    license_title = models.CharField(max_length=250, null=True)
    license_url = models.URLField(max_length=2000, null=True)
    language_code = models.CharField(max_length=100, null=True)
    duration = models.CharField(max_length=100, null=True)
    number = models.IntegerField(null=True)
    disc_number = models.IntegerField(null=True)
    explicit = models.CharField(max_length=100, null=True)
    explicit_notes = models.TextField(null=True)
    copyright_c = models.CharField(max_length=200, null=True)
    copyright_p = models.CharField(max_length=200, null=True)
    composer = models.CharField(max_length=250, null=True)
    lyricist = models.CharField(max_length=250, null=True)
    publisher = models.CharField(max_length=250, null=True)
    instrumental = models.NullBooleanField()
    information = models.CharField(max_length=250, null=True)
    date_recorded = models.DateField(null=True)
    comments = models.IntegerField(null=True)
    favorites = models.IntegerField(null=True)
    listens = models.IntegerField(null=True)
    interest = models.IntegerField(null=True)
    bit_rate = models.IntegerField(null=True)
    date_created = models.CharField(max_length=100, null=True)
    file = models.CharField(max_length=250, null=True)
    license_image_file = models.URLField(max_length=2000, null=True)
    license_image_file_large = models.URLField(max_length=2000, null=True)
    license_parent_id = models.IntegerField(null=True)
    tags = jsonfield.JSONField(null=True)
    genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title
