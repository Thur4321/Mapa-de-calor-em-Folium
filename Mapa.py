import folium
import pandas as pd
from PyQt5 import QtWidgets, QtWebEngineWidgets
from folium import plugins
import sys

m = folium.Map(location=[-23.547,-46.635], tiles=None, zoom_start=8)
df = pd.read_csv("data.csv", sep = ';', usecols = ['uf', 'nomeEstacao', 'latitude', 'datahora'])
df1 = df.replace({',':'.'}, regex = True)
df1['datahora'] = df1['datahora'].astype(float, errors = 'raise')
coordenadas = []
df2 = df1.groupby(['uf', 'nomeEstacao', 'latitude']).agg({'datahora':'sum'}).reset_index()
estacoes = folium.FeatureGroup('Estações')
mapaCalor = folium.FeatureGroup('Mapa de calor')

for lat, lon, pes, name in zip(df2.nomeEstacao, df2.latitude, df2.datahora, df2.uf):
    coordenadas.append([lon, lat, pes])
    estacoes.add_child(folium.Marker(location = [lon, lat], popup = f'Estação: '+name+'\nQuantidade (em mm): '+str(round(pes, 2))))
    
mapaCalor.add_child(plugins.HeatMap(coordenadas))
m.add_child(mapaCalor)
m.add_child(estacoes)
folium.LayerControl().add_to(m)

app = QtWidgets.QApplication(sys.argv)

w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(m.get_root().render())
w.resize(1280, 720)
w.setWindowTitle('Mapa')

w.show()
sys.exit(app.exec_())
