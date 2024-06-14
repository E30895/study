import pandas as pd

pd.set_option('display.float_format', '{:.2f}'.format)

df_observados = pd.read_excel('dados.xlsx')
df_projecoes = pd.read_excel('projecao.xlsx')

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


###########################

import pandas as pd

# Definir a formatação de exibição para floats
pd.set_option('display.float_format', '{:.2f}'.format)

# Carregar os dados dos arquivos Excel
df_observados = pd.read_excel('dados.xlsx')
df_projecoes = pd.read_excel('projecao.xlsx')

# Combinar os dois dataframes baseando-se nas colunas 'anomes' e 'ag'
df_merged = pd.merge(df_projecoes, df_observados, on=['anomes', 'ag'], how='left', suffixes=('_proj', '_obs'))

# Criar um dataframe final com as colunas desejadas
final = pd.DataFrame()
final[['anomes', 'ag', 'Ano', 'Mês', 'COOP']] = df_merged[['anomes', 'ag', 'Ano', 'Mês', 'COOP']]

# Sobrepor os valores observados sobre as projeções onde houver dados observados
final['rec_op'] = df_merged['rec_op_obs'].combine_first(df_merged['rec_op_proj'])
final['des_op'] = df_merged['des_op_obs'].combine_first(df_merged['des_op_proj'])
final['sob_liq'] = df_merged['sob_liq_obs'].combine_first(df_merged['sob_liq_proj'])
final['pr_liq'] = df_merged['pr_liq_obs'].combine_first(df_merged['pr_liq_proj'])
final['ind_liq'] = df_merged['ind_liq_obs'].combine_first(df_merged['ind_liq_proj'])
final['mg_rwa'] = df_merged['mg_rwa_obs'].combine_first(df_merged['mg_rwa_proj'])
final['roe'] = df_merged['roe_obs'].combine_first(df_merged['roe_proj'])

# Criar a coluna 'semestre' baseando-se na coluna 'anomes'
final['semestre'] = final['anomes'].map(lambda x: str(x).replace("2024", ""))
final['semestre'] = pd.to_numeric(final['semestre'])
final['semestre'] = ((final['semestre'] - 1) // 6) + 1

# Calcular a soma acumulada trimestral para cada pessoa no dataframe de projeções
# Considerando que a coluna 'COOP' representa as pessoas
# Vamos usar apenas os valores projetados para a soma acumulada
df_proj = df_projecoes.copy()
df_proj['trimestre'] = ((df_proj['anomes'] % 100 - 1) // 3) + 1

df_proj['rec_op_acumulado'] = df_proj.groupby(['trimestre', 'COOP'])['rec_op'].cumsum()
df_proj['des_op_acumulado'] = df_proj.groupby(['trimestre', 'COOP'])['des_op'].cumsum()

# Agora, combinamos novamente com o dataframe final para adicionar os valores acumulados
final = pd.merge(final, df_proj[['anomes', 'COOP', 'rec_op_acumulado', 'des_op_acumulado']], on=['anomes', 'COOP'], how='left')

# Substituir os valores acumulados calculados somente para os que não são observados
final['rec_op_acumulado'] = final.apply(lambda row: row['rec_op'] if not pd.isna(row['rec_op_obs']) else row['rec_op_acumulado'], axis=1)
final['des_op_acumulado'] = final.apply(lambda row: row['des_op'] if not pd.isna(row['des_op_obs']) else row['des_op_acumulado'], axis=1)

# Salvar o dataframe final em um arquivo Excel
final.to_excel('9_final_teste.xlsx', index=False)
