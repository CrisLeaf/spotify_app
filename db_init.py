import psycopg2
from secrets import psql_params


def reset_tables():
	commands = (
		"""
		DROP TABLE IF EXISTS tracks
		""",
		"""
		DROP TABLE IF EXISTS artists
		""",
		"""
		CREATE TABLE artists (
			artist_id SERIAL PRIMARY KEY,
			name VARCHAR (200) UNIQUE,
			genres VARCHAR (200),
			popularity INT
		)
		""",
		"""
		CREATE TABLE tracks (
			track_id SERIAL PRIMARY KEY,
			name VARCHAR (200),
			popularity INT,
			album TEXT,
			acousticness FLOAT,
			danceability FLOAT,
			duration_ms INT,
			energy FLOAT,
			instrumentalness FLOAT,
			key INT,
			liveness FLOAT,
			loudness FLOAT,
			mode INT,
			speechiness FLOAT,
			tempo FLOAT,
			time_signature INT,
			valence FLOAT,
			artist_id INT,
			CONSTRAINT fk_artist FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
		)
		"""
	)
	
	conn = psycopg2.connect(**psql_params)
	curr = conn.cursor()
	
	for command in commands:
		curr.execute(command)
	
	print("Base de datos creada")
	
	conn.commit()
	curr.close()
	conn.close()


if __name__ == "__main__":
	reset_tables()