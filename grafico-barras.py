import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults();
import mplcursors 

data_inep = pd.read_csv('microdados/microdados_ed_basica_2023.csv',encoding='latin-1', delimiter=';', low_memory=False, dtype={'coluna_31': str})
 
totalEscolas = len(data_inep)
escolasPorDependencia = data_inep['TP_DEPENDENCIA'].value_counts()
escolasPorDependencia.index = ['Municipais', 'Estaduais', 'Privadas', 'Federais']
porcentagens = (escolasPorDependencia / totalEscolas) * 100

plt.figure(figsize=(10, 6,))
bars = escolasPorDependencia.plot(kind='bar', color=['#5086c1', '#6a9eda', '#84b6f4' ,'#b2dafa'])

plt.title('Número de escolas por rede de ensino no Brasil em 2023', fontsize=16)
plt.ylabel('Número de escolas', fontsize=14)
plt.xlabel('Rede de ensino', fontsize=14)

plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

cursor = mplcursors.cursor(bars, hover=True)

@cursor.connect("add")
def on_add(sel):
    index = sel.index
    sel.annotation.set_text(f'{escolasPorDependencia[index]} escolas\n({porcentagens[index]:.2f}%)')
    sel.annotation.arrowprops = None
    sel.annotation.get_bbox_patch().set(fc="lightgray", lw=0)

plt.show()

