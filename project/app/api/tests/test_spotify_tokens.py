import spotipy
from spotipy import oauth2

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
def test_spotify_redirect(test_app):
    redirect_uri = spotipy.
    assert response.status_code == 302
    assert response.json() == {"environment": "dev", "responds": True, "testing": True}
