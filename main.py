from api.tracks import get_track, get_tracks, get_track_audio_features, get_tracks_audio_features
from api.artists import get_artist_top_tracks, get_artist
from api.albums import get_album, get_albums, get_album_tracks

# print(get_track('7ouMYWpwJ422jRcDASZB7P', 'US'))
# print(get_tracks(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ', '2takcwOaAZWiXQijPHIx7B'], 'US'))
# print(get_track_audio_features('7ouMYWpwJ422jRcDASZB7P'))
# print(get_tracks_audio_features(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ', '2takcwOaAZWiXQijPHIx7B']))

print(get_album('4aawyAB9vmqN3uQ7FjRGTy', 'US'))
print(get_albums(['382ObEPsp2rxGrnsizN5TX', '1A2GTWGtFfWp7KSQTwWOyo', '2noRn2Aes5aoNVsU6iWThc'], 'US'))
print(get_album_tracks('4aawyAB9vmqN3uQ7FjRGTy', 'US'))

# print(get_album('4aawyAB9vmqN3uQ7FjRGTy'))
# print(get_artist_top_tracks('0TnOYISbd1XYRBk9myaseg', 'US'))
