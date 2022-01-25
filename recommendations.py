import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import streamlit as st


class SpotifyRecommendations():
	
	def __init__(self, client_id, client_secret):
		self.client_id = st.secrets["client_id"]
		self.client_secret = st.secrets["client_secret"]
	
	def connect(self):
		client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id,
															  client_secret=self.client_secret)
		self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
		
		return self
	
	def artist_recommendation(self, artist_id: str, num_of_recomendations: int=5):
		related_artists = self.sp.artist_related_artists(artist_id)
		
		artists_ids = []
		artists_names = []
		artists_popularities = []
		
		for artist in related_artists["artists"]:
			artists_ids.append(artist["id"])
			artists_names.append(artist["name"])
			artists_popularities.append(artist["popularity"])
		
		candidates_df = pd.DataFrame({
			"id": artists_ids,
			"name": artists_names,
			"popularity": artists_popularities
		}).sort_values(by="popularity", ascending=False)
		
		return candidates_df[0:num_of_recomendations]


if __name__ == "__main__":
	spot_rec = SpotifyRecommendations(client_id, client_secret)
	spot_rec.connect()
	print(spot_rec.artist_recommendation("73SBwOgH6mrS09OyFHdR62"))