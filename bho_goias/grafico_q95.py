import pandas as pd 
import geopandas as gpd
import plotly.express as px

bho = pd.read_parquet('D:\\matheus.cgomes\\Documentos\\GitHub\\gis_automations\\data\\bho_q95_qmed_correc_29-05-2024_final_parquet_grafico.parquet')
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

meiaponte = filter_areamont(bho,'86999513','86') #alterar aqui 


teste = seleciona_jusante(meiaponte,'869999994') #alterar aqui = informe o cobacia a partir do qual deseja selcionar jusante

trechos_filtered = teste[['cobacia','nuareamont','new_q95_jan_ls', 'new_q95_fev_ls', 'new_q95_mar_ls',
       'new_q95_abr_ls', 'new_q95_mai_ls', 'new_q95_jun_ls', 'new_q95_jul_ls', 'new_q95_ago_ls',
       'new_q95_set_ls', 'new_q95_out_ls', 'new_q95_nov_ls', 'new_q95_dez_ls']]

melted_trechos = pd.melt(trechos_filtered,id_vars=['nuareamont','cobacia'],value_vars=trechos_filtered.columns,var_name='mes')
melted_trechos['mes'] = melted_trechos['mes'].map({
        'new_q95_jan_ls': 'Janeiro',
        'new_q95_fev_ls': 'Fevereiro',
        'new_q95_mar_ls': 'Março',
        'new_q95_abr_ls': 'Abril',
        'new_q95_mai_ls': 'Maio',
        'new_q95_jun_ls': 'Junho',
        'new_q95_jul_ls': 'Julho',
        'new_q95_ago_ls': 'Agosto',
        'new_q95_set_ls': 'Setembro',
        'new_q95_out_ls': 'Outubro',
        'new_q95_nov_ls': 'Novembro',
        'new_q95_dez_ls': 'Dezembro',
    })

graph = px.line(melted_trechos,x='nuareamont',y='value',color='mes',hover_data={'cobacia':True})

#APENAS SE FOR PARA A CALHA PRINCIPAL DO MEIA PONTE, CASO CONTRÁRIO COMENTAR
'''graph.add_vline(x=533.61, line_width=3, line_dash="dash", line_color="green",annotation_text='Inhumas')
graph.add_vline(x=1746.5565538516546, line_width=3, line_dash="dash", line_color="green",annotation_text='Montante Goiânia')
graph.add_vline(x=2834.1701695772012, line_width=3, line_dash="dash", line_color="green",annotation_text='Jusante Goiânia')
graph.add_vline(x=9595.019916024192, line_width=3, line_dash="dash", line_color="green",annotation_text='Aloândia')
graph.add_vline(x=12327.436831248671, line_width=3, line_dash="dash", line_color="green",annotation_text='Foz')'''


graph.show()








    