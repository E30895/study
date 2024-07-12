df <- df %>%
  mutate(
    semestre = case_when(
      substr(as.character(ano_mes), 5, 6) %in% c("01", "02", "03", "04", "05", "06") ~ paste0(substr(as.character(ano_mes), 1, 4), "-S1"),
      substr(as.character(ano_mes), 5, 6) %in% c("07", "08", "09", "10", "11", "12") ~ paste0(substr(as.character(ano_mes), 1, 4), "-S2")
    )
  )

# Calculando a soma acumulada para os dados projetados
df_projetado_acumulado <- df_projetado %>%
  arrange(ag, ano_mes) %>%
  group_by(ag, semestre) %>%
  mutate(acumulado_projetado = cumsum(valor_projetado)) %>%
  ungroup()

# Mesclando com dados realizados
df_combined <- df_projetado_acumulado %>%
  left_join(df_realizado, by = c("ano_mes", "ag", "semestre")) %>%
  mutate(
    acumulado_realizado = ifelse(is.na(valor_realizado), NA, valor_realizado),
    acumulado_final = ifelse(is.na(acumulado_realizado),
                             acumulado_projetado + lag(acumulado_final, default = 0),
                             acumulado_realizado)
  ) %>%
  group_by(ag, semestre) %>%
  mutate(acumulado_final = cumsum(acumulado_final)) %>%
  ungroup()

