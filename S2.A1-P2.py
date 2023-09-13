import pandas as pd

url = "https://raw.githubusercontent.com/sundeepblue/movie_rating_prediction/master/movie_metadata.csv"
df = pd.read_csv(url,header=0,index_col=False)

# PUNTO 1. COL gross EN VAL NULOS IGUAL AL PROMEDIO DE ESA COL
df['gross'] = df['gross'].fillna(df['gross'].mean())

# PUNTO 2. COL facenumber_in_poster CAMBIAR VALORES NULOS Y NEGATIVOS POR 0
df['facenumber_in_poster'] = df['facenumber_in_poster'].fillna(0).replace([df['facenumber_in_poster'][df['facenumber_in_poster'] < 0]],0)

# PUNTO 3. CREAR NUVA COLUMNA TittleCode EXTRAYENDO EL CODIGO DE LA CADENA (link) DE LA COL movie_imdb_link
df['TittleCode'] = df['movie_imdb_link'].str.split('title/',expand=True)[1].str.split('/',expand=True)[0]

# PUNTO 4. COL title_year CAMBIAR VALORES NULOS POR 0
df['title_year'] = df['title_year'].fillna(0)

# PUNTO 5. PELICULAS FIRMADAS EN USA
df = df[df['country'] == 'USA']

# RUTA DE EXPORTACION DE ARCHIVO
url = "data/FilmTV_USAMovies.csv"

# EXPORTANDO ARCUVO EN FORMATO CSV
df.to_csv(url,index=False)