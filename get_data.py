import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secrets import client_id, client_secret


# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
													  client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#%%
playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DWSpF87bP6JSF"
playlist_uri = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_uri)["items"]]

#%%
data = {}
for track in sp.playlist_tracks(playlist_uri)["items"][49:50]:
	# URI
	data["track_uri"] = track["track"]["uri"]
	
	# Track Name
	data["track_name"] = track["track"]["name"]
	
	# Artists
	for index, artist in enumerate(track["track"]["artists"]):
		data[f"artist_name_{index + 1}"] = artist["name"]
		
		artist_uri = artist["uri"]
		artist_info = sp.artist(artist_uri)
		
		data[f"artist_pop_{index + 1}"] = artist_info["popularity"]
		data[f"artist_genres_{index + 1}"] = artist_info["genres"]
	
	# Album
	data["album"] = track["track"]["album"]["name"]
	
	# Popularity of the track
	data["track_pop"] = track["track"]["popularity"]
	
	data["audio_features"] = sp.audio_features(data["track_uri"])[0]

