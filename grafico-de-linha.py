import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

files = [
    'microdados/microdados_ed_basica_2023.csv',
    'microdados/microdados_ed_basica_2022.csv',
    'microdados/microdados_ed_basica_2021.csv',
    'microdados/microdados_ed_basica_2020.csv',
    'microdados/microdados_ed_basica_2019.csv'
]
dataframes = [pd.read_csv(file, encoding='latin-1', delimiter=';', low_memory=False) for file in files]
data_inep = pd.concat(dataframes)

grouped_data = data_inep.groupby(['NU_ANO_CENSO', 'TP_DEPENDENCIA'])['QT_MAT_MED'].sum().unstack(fill_value=0)
grouped_data.columns = ['Federais', 'Estaduais', 'Municipais', 'Privadas']
grouped_data.index = pd.to_datetime(grouped_data.index, format='%Y').strftime('%Y')

plt.figure(figsize=(12, 8))

lines = []
for column in grouped_data.columns:
    line, = plt.plot(grouped_data.index, grouped_data[column], marker='o', label=column)
    lines.append(line)

plt.title('Evolução no número de matrículas do ensino medio por rede de ensino nos últimos 5 anos', fontsize=16)
plt.xlabel('Anos', fontsize=14)
plt.ylabel('Quantidade de Matrículas', fontsize=14)
plt.xticks(rotation=0)
plt.tight_layout()

plt.legend(title='rede de ensino')

cursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_hover(sel):
    index = grouped_data.index[int(sel.target[0])]
    value = int(sel.target[1])
    sel.annotation.set(text=f"{sel.artist.get_label()}\nAno: {index}\nMatrículas: {value}")
    sel.annotation.arrowprops = None
    sel.annotation.get_bbox_patch().set(fc="lightgray", lw=0)

plt.show()
