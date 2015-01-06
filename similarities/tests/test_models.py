from unittest import TestCase
from unittest.mock import patch

from django.test import TestCase as DjangoTestCase

from artists.models import Artist
from artists.tests.factories import HyperlinkFactory
from . import factories
from .. import models


class GeneralArtistModelTest(TestCase):

    """Tests for GeneralArtist model."""

    def test_save(self):
        name = "Brad Sucks"
        artist = models.GeneralArtist(name=name)
        with patch('similarities.models.GeneralArtist.save_base') as save_base:
            assert artist.normalized_name == ""
            artist.save()
            save_base.assert_called_once_with(
                update_fields=None,
                using='default',
                force_update=False,
                force_insert=False,
            )
            assert artist.normalized_name == name.upper()


class CreateGeneralArtistTest(DjangoTestCase):

    """Tests for create_general_artist post_save handler."""

    name = "Brad Sucks"
    normalized_name = name.upper()

    def test_insert(self):
        artist = Artist.objects.create(name=self.name)
        general_artist = models.GeneralArtist.objects.get()
        similarity = models.Similarity.objects.get()
        assert general_artist.name == self.name
        assert general_artist.normalized_name == self.normalized_name
        assert similarity.cc_artist == artist
        assert similarity.other_artist == general_artist
        assert similarity.weight == 5

    def test_update(self):
        artist = Artist.objects.create(name=self.name)
        models.GeneralArtist.objects.all().delete()
        models.Similarity.objects.all().delete()
        artist.save()
        assert not models.GeneralArtist.objects.exists()
        assert not models.Similarity.objects.exists()


class BaseSimilarityModelTest(TestCase):

    """Tests for BaseSimilarity model."""

    def test_weights(self):
        assert (list(models.BaseSimilarity.WEIGHTS) == [
            (0, 'dissimilar (these artists are not similar at all)'),
            (1, "slightly similar (they're not completely different)"),
            (2, 'fairly similar (some elements of the music sound similar)'),
            (3, 'very similar (fans of one probably like the other)'),
            (4, 'extremely similar (easily mistakable)'),
            (5, 'identical (different name for the same artist)'),
        ])

    def test_default_weight(self):
        assert models.BaseSimilarity().weight == 0


class SimilarityManagerTest(DjangoTestCase):

    """Tests for SimilarityManager."""

    def test_low_track_count(self):
        link = HyperlinkFactory(num_tracks=0)
        user_similarity = factories.UserSimilarityFactory(
            weight=5, cc_artist=link.artist)
        similarity, _ = models.Similarity.objects.update_or_create_by_artists(
            other_artist=user_similarity.other_artist,
            cc_artist=user_similarity.cc_artist)
        assert similarity.weight == 0

    def test_high_track_count(self):
        link = HyperlinkFactory(num_tracks=20)
        user_similarity = factories.UserSimilarityFactory(
            weight=5, cc_artist=link.artist)
        similarity, _ = models.Similarity.objects.update_or_create_by_artists(
            other_artist=user_similarity.other_artist,
            cc_artist=user_similarity.cc_artist)
        assert similarity.weight == 5

    def test_no_track_count(self):
        link = HyperlinkFactory(num_tracks=None)
        user_similarity = factories.UserSimilarityFactory(
            weight=5, cc_artist=link.artist)
        similarity, _ = models.Similarity.objects.update_or_create_by_artists(
            other_artist=user_similarity.other_artist,
            cc_artist=user_similarity.cc_artist)
        assert similarity.weight == 5
