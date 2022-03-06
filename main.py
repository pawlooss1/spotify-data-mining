from api.albums import get_album, get_albums, get_album_tracks
from api.artists import get_artist_top_tracks, get_artist, get_artists, get_artist_albums, get_related_artists
from api.tracks import get_track, get_tracks, get_track_audio_features, get_tracks_audio_features

print(get_track('7ouMYWpwJ422jRcDASZB7P', 'US'))
print(get_tracks(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ', '2takcwOaAZWiXQijPHIx7B'], 'US'))
print(get_track_audio_features('7ouMYWpwJ422jRcDASZB7P'))
print(get_tracks_audio_features(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ', '2takcwOaAZWiXQijPHIx7B']))
print()
print(get_album('4aawyAB9vmqN3uQ7FjRGTy', 'US'))
print(get_albums(['382ObEPsp2rxGrnsizN5TX', '1A2GTWGtFfWp7KSQTwWOyo', '2noRn2Aes5aoNVsU6iWThc'], 'US'))
print(get_album_tracks('4aawyAB9vmqN3uQ7FjRGTy', 'US'))
print()
print(get_artist('0TnOYISbd1XYRBk9myaseg'))
print(get_artists(['2CIMQHirSU0MQqyYHq0eOx', '57dN52uHvrHOxijzpIgu3E', '1vCWHaC5f2uS3yhpwWbIA6']))
print(get_artist_albums('0TnOYISbd1XYRBk9myaseg'))
print(get_artist_top_tracks('0TnOYISbd1XYRBk9myaseg', 'US'))
print(get_related_artists('0TnOYISbd1XYRBk9myaseg'))
