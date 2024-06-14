import pandas as pd

pd.set_option('display.float_format', '{:.2f}'.format)

df_observados = pd.read_excel('1_Dados_202404.xlsx')
df_projecoes = pd.read_excel('1_Projecoes_tesouraria.xlsx')

df_merged = pd.merge(df_projecoes, df_observados, on=['anomes','ag'], how='left', suffixes=('_proj', '_obs'))

final = pd.DataFrame()
final[['anomes', 'ag', 'Ano', 'Mês', 'COOP']] = df_merged[['anomes', 'ag', 'Ano', 'Mês', 'COOP']]

final['rec_op'] = df_merged['rec_op_obs'].combine_first(df_merged['rec_op_proj'])
final['des_op'] = df_merged['des_op_obs'].combine_first(df_merged['des_op_proj'])
final['sob_liq'] = df_merged['sob_liq_obs'].combine_first(df_merged['sob_liq_proj'])
final['pr_liq'] = df_merged['pr_liq_obs'].combine_first(df_merged['pr_liq_proj'])
final['ind_liq'] = df_merged['ind_liq_obs'].combine_first(df_merged['ind_liq_proj'])
final['mg_rwa'] = df_merged['mg_rwa_obs'].combine_first(df_merged['mg_rwa_proj'])
final['roe'] = df_merged['roe_obs'].combine_first(df_merged['roe_proj'])

final['semestre'] = final['anomes'].map(lambda x:str(x).replace("2024", ""))
final['semestre'] = pd.to_numeric(final['semestre'])
final['semestre'] = ((final['semestre'] - 1) //6) + 1
#final['semestre'] = final['semestre'].map(lambda x:str(x))

final['rec_op'] = final.groupby(['semestre', 'ag'])['rec_op'].cumsum()
final['des_op'] = final.groupby(['semestre', 'ag'])['des_op'].cumsum()

final.to_excel('9_final_teste.xlsx', index=False)
