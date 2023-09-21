import pandas as pd
import folium as f
import PIL.Image as pimg
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer

url = '../RESOURCE/newYorkCityArtGalleries.csv'
df = pd.read_csv(url,header=0,index_col=False)

# PUNTO 1 - ELIMINAR REGISTROS DUPLICADOS
# PUNTO 2 - ELIMINAR COLUMNA DIRECCION 2

df = df.drop_duplicates().drop('ADDRESS2', axis='columns')

# PUNTO 3 - MUSEOS O GALERIAS DE BROOKLYN

brooklyn = df[['CITY', 'NAME']][(df['CITY'] == 'Brooklyn') & (df['NAME'].str.contains('Museum | Gallery'))]

# EXPRTAR ARCIVO CSV

csv = df[(df['CITY'] == 'Brooklyn') & (df['NAME'].str.contains('Museum | Gallery'))].sort_values('GRADING',ascending=False)
url = "newYorkCityArtGalleriesGrading.csv"
csv.to_csv(url,index=False)

# PUNTO 4 - 3 MEJORES CALIFICADOS (museo o galería)

brooklynTop = df[['CITY', 'NAME', 'GRADING']][(df['CITY'] == 'Brooklyn') & (df['NAME'].str.contains('Museum | Gallery'))].sort_values('GRADING',ascending=False).head(3)

# PUNTO 5 - IMAGEN MAPA INDICNDO TOP 3 (museo o galería)

brooklynTop = df[['CITY', 'NAME', 'GRADING', 'ADDRESS1', 'the_geom']][(df['CITY'] == 'Brooklyn') & (df['NAME'].str.contains('Museum | Gallery'))].sort_values('GRADING',ascending=False).head(3).reset_index(drop=True)

coords = brooklynTop['the_geom'].str.split(pat = 'POINT \(|\)',expand=True)[1].str.split(pat = ' ',expand=True)

map = f.Map(location=[coords.loc[2][1],coords.loc[2][0]], zoom_start = 11.5)

for row in coords.iterrows():
    f.Marker(location = [row[1][1], row[1][0]], icon=f.Icon(color = "blue", icon = "star")).add_to(map)

map.save('temp_map.html')

dataImg = map._to_png()
img = pimg.open(io.BytesIO(dataImg))
img.save('temp_map.png')

# PUNTO 6 - GENERAR RREPORTE FINAL (PDF)

pdf = SimpleDocTemplate("informe_final.pdf", pagesize=letter)

styles = getSampleStyleSheet()
datos = []

titulo = " MEJORES MUSEOS Y GALERIAS DE BROOKLYN"
datos.append(Paragraph(titulo, styles["Title"]))

mapaImg = Image("temp_map.png", width=500, height=300)
datos.append(mapaImg)


font = ParagraphStyle(name='Normal', fontSize=12)
for index, row in brooklynTop.iterrows():
    texto = f"<br/>NOMBRE: {row['NAME']}<br/>DIRECCION: {row['ADDRESS1']}<br/>CALIFICACION: {row['GRADING']}"
    datos.append(Spacer(1, 8))
    datos.append(Paragraph(texto,font))

pdf.build(datos)