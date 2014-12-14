from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, null=True)
    url = models.URLField(unique=True)
    location = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=255, null=True)
    artist = models.ForeignKey(Artist, null=True)
    url = models.URLField(unique=True)
    art = models.URLField(null=True)
    release_date = models.CharField(max_length=100, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)
    as_of = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
