from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from model_utils import Choices
from model_utils.models import TimeStampedModel


class GeneralArtist(TimeStampedModel):

    """Any artist that might be searched for."""

    name = models.CharField(max_length=100, unique=True)
    normalized_name = models.CharField(max_length=100, editable=False,
                                       unique=True)
    similar_artists = models.ManyToManyField(to='artists.Artist',
                                             through='Similarity')

    def save(self, **kwargs):
        self.normalized_name = self.name.upper()
        return super().save(**kwargs)

    def __str__(self):
        return self.name


def create_general_artist(instance, created, **kwargs):
    if created:
        artist, _ = GeneralArtist.objects.get_or_create(
            normalized_name=instance.name.upper(),
            defaults={'name': instance.name},
        )
        Similarity.objects.get_or_create(cc_artist=instance,
                                         other_artist=artist, weight=5)


post_save.connect(create_general_artist, 'artists.Artist')


class BaseSimilarity(TimeStampedModel):

    class Meta:
        abstract = True

    WEIGHTS = Choices(
        (0, "dissimilar (these artists are not similar at all)"),
        (1, "slightly similar (they're not completely different)"),
        (2, "fairly similar (some elements of the music sound similar)"),
        (3, "very similar (fans of one probably like the other)"),
        (4, "extremely similar (easily mistakable)"),
        (5, "identical (different name for the same artist)"),
    )

    cc_artist = models.ForeignKey('artists.Artist', verbose_name="CC artist")
    other_artist = models.ForeignKey(GeneralArtist)
    weight = models.FloatField(choices=WEIGHTS, default=0)


class UserSimilarity(BaseSimilarity):

    """Similarity between two artists as given by an individual user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name_plural = "user similarities"
        unique_together = (
            ('user', 'cc_artist', 'other_artist'),
        )

    def save(self, *args, **kwargs):
        other_artists_to_update = []
        if self.pk:
            prev_other_artist = type(self).objects.get(pk=self.pk).other_artist
        else:
            prev_other_artist = None
        super().save(*args, **kwargs)
        if self.other_artist:
            other_artists_to_update.append(self.other_artist)
        if prev_other_artist and self.other_artist != prev_other_artist:
            other_artists_to_update.append(prev_other_artist)
        for other in other_artists_to_update:
            Similarity.objects.update_or_create_by_artists(
                other_artist=other,
                cc_artist=self.cc_artist,
            )


class SimilarityManager(models.Manager):

    def update_or_create_by_artists(self, other_artist, cc_artist):
        if other_artist.normalized_name == cc_artist.name.upper():
            weight = 5
        else:
            weight = (UserSimilarity.objects
                      .filter(other_artist=other_artist,
                              cc_artist=cc_artist)
                      .aggregate(models.Avg('weight')))['weight__avg'] or 0
        return self.update_or_create(
            other_artist=other_artist,
            cc_artist=cc_artist,
            defaults={'weight': weight},
        )


class Similarity(BaseSimilarity):

    """Cummulative similarity between two artists."""

    class Meta:
        verbose_name_plural = "similarities"
        unique_together = (
            ('cc_artist', 'other_artist'),
        )

    objects = SimilarityManager()
