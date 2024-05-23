import pandas as pd 
import geopandas as gpd
import plotly.express as px

bho = pd.read_parquet('D:\\BHO_GOIAS\\bho_q95_qmed_correc_22-05-2024.parquet')
bho['cocursodag'] = bho['cocursodag'].astype(str)
bho['cobacia'] = bho['cobacia'].astype(str)
bho['cobacia_jus'] = bho['cobacia_jus'].astype(str)



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

meiaponte = filter_areamont(bho,'8696111','8696') #alterar aqui 


teste = seleciona_jusante(meiaponte,'869698895') #alterar aqui = informe o cobacia a partir do qual deseja selcionar jusante

trechos_filtered = teste[['cobacia','nuareamont','new_qmed_jan_ls', 'new_qmed_fev_ls', 'new_qmed_mar_ls',
       'new_qmed_abr_ls', 'new_qmed_mai_ls', 'new_qmed_jun_ls', 'new_qmed_jul_ls', 'new_qmed_ago_ls',
       'new_qmed_set_ls', 'new_qmed_out_ls', 'new_qmed_nov_ls', 'new_qmed_dez_ls']]

melted_trechos = pd.melt(trechos_filtered,id_vars=['nuareamont','cobacia'],value_vars=trechos_filtered.columns,var_name='mes')
melted_trechos['mes'] = melted_trechos['mes'].map({
        'new_qmed_jan_ls': 'Vazão Média - Janeiro',
        'new_qmed_fev_ls': 'Vazão Média - Fevereiro',
        'new_qmed_mar_ls': 'Vazão Média - Março',
        'new_qmed_abr_ls': 'Vazão Média - Abril',
        'new_qmed_mai_ls': 'Vazão Média - Maio',
        'new_qmed_jun_ls': 'Vazão Média - Junho',
        'new_qmed_jul_ls': 'Vazão Média - Julho',
        'new_qmed_ago_ls': 'Vazão Média - Agosto',
        'new_qmed_set_ls': 'Vazão Média - Setembro',
        'new_qmed_out_ls': 'Vazão Média - Outubro',
        'new_qmed_nov_ls': 'Vazão Média - Novembro',
        'new_qmed_dez_ls': 'Vazão Média - Dezembro',
    })

graph = px.line(melted_trechos,x='nuareamont',y='value',color='mes',hover_data={'cobacia':True})

#APENAS SE FOR PARA A CALHA PRINCIPAL DO MEIA PONTE, CASO CONTRÁRIO COMENTAR
'''graph.add_vline(x=533.61, line_width=3, line_dash="dash", line_color="green",annotation_text='Inhumas')
graph.add_vline(x=1746.5565538516546, line_width=3, line_dash="dash", line_color="green",annotation_text='Montante Goiânia')
graph.add_vline(x=2834.1701695772012, line_width=3, line_dash="dash", line_color="green",annotation_text='Jusante Goiânia')
graph.add_vline(x=9595.019916024192, line_width=3, line_dash="dash", line_color="green",annotation_text='Aloândia')
graph.add_vline(x=12327.436831248671, line_width=3, line_dash="dash", line_color="green",annotation_text='Foz')'''


graph.show()







    