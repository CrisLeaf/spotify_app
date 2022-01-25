import streamlit as st
from recommendations import SpotifyRecommendations
from token_secrets import client_id, client_secret


def main():
	html_header = """
		<head>
		<link rel="stylesheet"href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"integrity="sha512-Fo3rlrZj/k7ujTnHg4CGR2D7kSs0v4LLanw2qksYuRlEzO+tcaEPQogQ0KaoGN26/zrn20ImR1DfuLWnOo7aBA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
		</head>
		<a href="https://crisleaf.github.io/apps.html">
			<i class="fas fa-arrow-left"></i>
		</a>
		<h2 style="text-align:center;">Sistema de Recomendación para Spotify</h2>
		<style>
			i {
				font-size: 30px;
				color: #222;
			}
			i:hover {
				color: cornflowerblue;
				transition: color 0.3s ease;
			}
		</style>
	"""
	st.markdown(html_header, unsafe_allow_html=True)
	
	spot_rec = SpotifyRecommendations(client_id, client_secret)
	spot_rec.connect()
	
	artist_id = st.text_input("Ingrese ID del Artista:")
	
	if st.button("Recomendar"):
		recommendations = spot_rec.artist_recommendation(artist_id)
		
		for id, name in zip(recommendations["id"], recommendations["name"]):
			html_source_code = f"""
						<p class="source-code-info">
						<a href="https://open.spotify.com/artist/{id}">{name}</a></p>
					"""
			st.markdown(html_source_code, unsafe_allow_html=True)
	
	html_source_code = """
		<p class="source-code">Código Fuente:
		<a href="https://github.com/CrisLeaf/spotify_recommendations_app">
		<i class="fab fa-github"></i></a></p>
		<style>
			.source-code {
				text-align: right;
				color: #666;
			}
			.fa-github {
				color: #666;
			}
		</style>
	"""
	st.markdown(html_source_code, unsafe_allow_html=True)


if __name__ == "__main__":
	main()