import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secrets import client_id, client_secret, psql_params
import psycopg2


def get_playlist_data(playlist_link):
	client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
														  client_secret=client_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	
	playlist_uri = playlist_link.split("/")[-1].split("?")[0]
	
	conn = psycopg2.connect(**psql_params)
	curr = conn.cursor()
	
	for track in sp.playlist_tracks(playlist_uri)["items"][48:49]:
		# Artists
		print(f"length: {len(track['track']['artists'])}")
		artist_ids = []
		
		for index, artist in enumerate(track["track"]["artists"]):
			artist_name = artist["name"]
			
			artist_uri = artist["uri"]
			artist_info = sp.artist(artist_uri)
			
			artist_genres = artist_info["genres"]
			artist_popularity = artist_info["popularity"]
			
			try:
				curr.execute("INSERT INTO artists (name, genres, popularity) VALUES (%s, %s, %s)",
							 (artist_name, artist_genres, artist_popularity))
			except:
				conn.rollback()
			
			curr.execute("SELECT artist_id FROM artists WHERE name = %s", (artist_name,))
			artist_id = curr.fetchall()[0][0]
			
			artist_ids.append(artist_id)
		
		# Tracks
		name = track["track"]["name"]
		popularity = track["track"]["popularity"]
		album = track["track"]["album"]["name"]
		
		track_uri = track["track"]["uri"]
		features = sp.audio_features(track_uri)[0]
		
		acousticness = features["acousticness"]
		danceability = features["danceability"]
		duration_ms = features["duration_ms"]
		energy = features["energy"]
		instrumentalness = features["instrumentalness"]
		key = features["key"]
		liveness = features["liveness"]
		loudness = features["loudness"]
		mode = features["mode"]
		speechiness = features["speechiness"]
		tempo = features["tempo"]
		time_signature = features["time_signature"]
		valence = features["valence"]
		
		for artist_id in artist_ids:
			curr.execute(
				"""
                INSERT INTO tracks (name, popularity, album, acousticness, danceability,
                                    duration_ms, energy, instrumentalness, key, liveness,
                                    loudness, mode, speechiness, tempo, time_signature, valence,
                                    artist_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
				(name, popularity, album, acousticness, danceability, duration_ms, energy,
				 instrumentalness, key, liveness, loudness, mode, speechiness, tempo,
				 time_signature, valence, artist_id)
			)
			
			conn.commit()
	
	curr.close()
	conn.close()
	

if __name__ == "__main__":
	playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DWSpF87bP6JSF"
	get_playlist_data(playlist_link)
	
	print("Datos ingresados exitosamente!")