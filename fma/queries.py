import purl
import requests
from django.conf import settings

from . import models

API_KEY = getattr(settings, 'FMA_API_KEY', None)


class FMAQueryException(Exception):
    """Base exception for errors querying the FMA API"""


class FMAServerError(FMAQueryException):
    """Raised when an error status code is found on a response from the FMA server"""


class FMAQueryError(FMAQueryException):
    """Error indicated in the API response, probably an error in the request"""


def query_tracks(artist=None):
    track_resource = "http://freemusicarchive.org/api/get/tracks.json"
    query_url = purl.URL(track_resource).query_params({
        'api_key': API_KEY,
        'artist_id': artist.pk,
        'limit': 20000,
    }).as_string()
    response = requests.get(query_url)
    if response.status_code >= 500:
        raise FMAServerError("Failed to query FMA artist due to server error.")
    track_data = response.json()
    if track_data['errors']:
        raise FMAQueryError("Error querying Free Music Archive: {}".format(track_data['errors']))
    return [track_from_json(t) for t in track_data['dataset']]


def track_from_json(data):
    artist, _ = models.Artist.objects.update_or_create(pk=data['artist_id'], defaults={
        'name': data['artist_name'],
        'url': data['artist_url'],
        'website': data['artist_website'],
    })
    if data['album_id']:
        album, _ = models.Album.objects.update_or_create(pk=data['album_id'], defaults={
            'title': data['album_title'],
            'url': data['album_url'],
            'artist': artist,
        })
    else:
        album = None
    track = models.Track(artist=artist, album=album)
    for field in track._meta.fields:
        try:
            try:
                value = data["track_{}".format(field.name)]
            except KeyError:
                value = data[field.name]
        except KeyError:
            pass
        else:
            setattr(track, field.name, value)
    track.instrumental = int(data['track_instrumental'])
    track.save()
    for genre_data in data.get('track_genres', []):
        genre, _ = models.Genre.objects.update_or_create(
            id=genre_data['genre_id'],
            title=genre_data['genre_title'],
            url=genre_data['genre_url']
        )
        track.genres.add(genre)
    return track
