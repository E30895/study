pip install pandas openpyxl
import pandas as pd

import pandas as pd

# Carregar as planilhas
df_projecoes = pd.read_excel('projecoes.xlsx')
df_observados = pd.read_excel('observados.xlsx')

# Mesclar as duas planilhas com base na coluna 'Data' e 'Indicador'
df_merged = pd.merge(df_projecoes, df_observados, on=['Data', 'Indicador'], how='left', suffixes=('_proj', '_obs'))

# Substituir os valores projetados pelos observados onde houver correspondência
df_merged['Valor'] = df_merged['Valor_obs'].combine_first(df_merged['Valor_proj'])

# Selecionar apenas as colunas necessárias para o resultado final
df_resultado = df_merged[['Data', 'Indicador', 'Valor']]

# Salvar o resultado em uma nova planilha
df_resultado.to_excel('resultado.xlsx', index=False)

print("Substituição concluída e resultado salvo em 'resultado.xlsx'")
