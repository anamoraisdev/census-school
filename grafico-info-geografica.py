import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import mplcursors

data_inep = pd.read_csv('microdados/microdados_ed_basica_2023.csv', encoding='latin-1', delimiter=';', low_memory=False, dtype={'coluna_31': str})
estados = gpd.read_file("microdados/brazil-states.geojson")
dependencias = {1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'}
data_inep['TP_DEPENDENCIA'] = data_inep['TP_DEPENDENCIA'].map(dependencias)

grouped_data = data_inep.groupby(['SG_UF', 'TP_DEPENDENCIA']).size().unstack(fill_value=0)

total_escolas_estado = grouped_data.sum(axis=1)
total_escolas_estado.name = 'total_escolas'

mapa_escolas = estados.merge(total_escolas_estado, how="left", left_on="sigla", right_index=True)

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
mapa_escolas.plot(column='total_escolas', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=False)

for idx, row in mapa_escolas.iterrows():
    centroid_x, centroid_y = row['geometry'].centroid.coords[0]
    plt.annotate(text=row['sigla'], xy=(centroid_x, centroid_y), xytext=(0, 0), textcoords="offset points", ha='center', fontsize=8)

max_escolas = mapa_escolas['total_escolas'].max()
handles = {}
for idx, row in mapa_escolas.iterrows():
    label = f"{row['total_escolas']} escolas"
    color = plt.cm.Blues(row['total_escolas'] / max_escolas)  
    handles[row['total_escolas']] = plt.Line2D([0], [0], marker='o', color='w', label=label, markerfacecolor=color, markersize=10)

sorted_keys = sorted(handles.keys(), reverse=True)

legend_handles = [handles[key] for key in sorted_keys]
legend_labels = [f"{key} escolas" for key in sorted_keys]
plt.legend(handles=legend_handles, labels=legend_labels,  loc='upper left', bbox_to_anchor=(1, 1))

def format_annotation(sel):
    x, y = sel.target
    sel.annotation.get_bbox_patch().set(fc="lightgray", lw=0)
    sel.annotation.arrowprops = None
    for i, row in mapa_escolas.iterrows():
       if row['geometry'].contains(Point(x, y)):
        state_name = row['sigla']
        total_schools = total_escolas_estado[state_name]
        federal = grouped_data.loc[state_name, 'Federal']
        estadual = grouped_data.loc[state_name, 'Estadual']
        municipal = grouped_data.loc[state_name, 'Municipal']
        privada = grouped_data.loc[state_name, 'Privada']
        return f"Estado: {state_name}\nTotal de Escolas: {total_schools}\nFederal: {federal}\nEstadual: {estadual}\nMunicipal: {municipal}\nPrivada: {privada}"
    sel.annotation.set_visible(False)

cursor = mplcursors.cursor(ax, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(format_annotation(sel)))

plt.title('Número de Escolas por Estado')
plt.show()




