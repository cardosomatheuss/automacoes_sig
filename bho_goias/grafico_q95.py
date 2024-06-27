import pandas as pd 
import geopandas as gpd
import plotly.express as px

bho = pd.read_csv('D:\\matheus.cgomes\\Documentos\\GitHub\\gis_automations\\data\\26-06-2024\\bho_goias_semad_linha_completa_26-06-2024.csv')
bho['cocursodag'] = bho['cocursodag'].astype(str)
bho['cobacia'] = bho['cobacia'].astype(str)
bho['cobacia_jus'] = bho['cobacia_jus'].astype(str)
bho['cobacia_jus'] = bho['cobacia_jus'].str.rstrip('.0')

bho.info(verbose=True)



geodataframe = gpd.GeoDataFrame()
def seleciona_jusante(bho,cod_cobacia): #recebe o poligono bho e uma string com o código otto (cobacia)
    global geodataframe
    if cod_cobacia in bho['cobacia'].values:
        trecho = bho[bho['cobacia']==(cod_cobacia)]
        geodataframe = pd.concat([geodataframe,trecho])
        for ind in trecho.index:
            
            seleciona_jusante(bho,trecho['cobacia_jus'][ind])
            return gpd.GeoDataFrame(geodataframe).reset_index(drop=True)
                    
    else:
        return gpd.GeoDataFrame(geodataframe).reset_index(drop=True)
    
def filter_areamont(bho,cobacia,cocursodag):
    filter_trechos = ((bho['cobacia']>=cobacia) & (bho['cocursodag'].str.startswith(cocursodag)))

    filtered = bho.loc[filter_trechos]

    return filtered

meiaponte = filter_areamont(bho,'8691611111','86916') #alterar aqui 


teste = seleciona_jusante(meiaponte,'8691696495') #alterar aqui = informe o cobacia a partir do qual deseja selcionar jusante

trechos_filtered = teste[['cobacia','nuareamont','q95_jan', 'q95_fev', 'q95_mar',
       'q95_abr', 'q95_mai', 'q95_jun', 'q95_jul', 'q95_ago',
       'q95_set', 'q95_out', 'q95_nov', 'q95_dez']]

melted_trechos = pd.melt(trechos_filtered,id_vars=['nuareamont','cobacia'],value_vars=trechos_filtered.columns,var_name='mes')
melted_trechos['mes'] = melted_trechos['mes'].map({
        'q95_jan': 'Janeiro',
        'q95_fev': 'Fevereiro',
        'q95_mar': 'Março',
        'q95_abr': 'Abril',
        'q95_mai': 'Maio',
        'q95_jun': 'Junho',
        'q95_jul': 'Julho',
        'q95_ago': 'Agosto',
        'q95_set': 'Setembro',
        'q95_out': 'Outubro',
        'q95_nov': 'Novembro',
        'q95_dez': 'Dezembro',
    })

graph = px.line(melted_trechos,x='nuareamont',y='value',color='mes',hover_data={'cobacia':True})

#APENAS SE FOR PARA A CALHA PRINCIPAL DO MEIA PONTE, CASO CONTRÁRIO COMENTAR
'''graph.add_vline(x=533.61, line_width=3, line_dash="dash", line_color="green",annotation_text='Inhumas')
graph.add_vline(x=1746.5565538516546, line_width=3, line_dash="dash", line_color="green",annotation_text='Montante Goiânia')
graph.add_vline(x=2834.1701695772012, line_width=3, line_dash="dash", line_color="green",annotation_text='Jusante Goiânia')
graph.add_vline(x=9595.019916024192, line_width=3, line_dash="dash", line_color="green",annotation_text='Aloândia')
graph.add_vline(x=12327.436831248671, line_width=3, line_dash="dash", line_color="green",annotation_text='Foz')'''


graph.show()








    