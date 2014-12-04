from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=255, null=True)
    url = models.URLField()
    art = models.URLField()
    release_date = models.DateField(blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)
    as_of = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
