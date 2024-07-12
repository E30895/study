df <- df %>%
  mutate(
    semestre = case_when(
      substr(as.character(ano_mes), 5, 6) %in% c("01", "02", "03", "04", "05", "06") ~ paste0(substr(as.character(ano_mes), 1, 4), "-S1"),
      substr(as.character(ano_mes), 5, 6) %in% c("07", "08", "09", "10", "11", "12") ~ paste0(substr(as.character(ano_mes), 1, 4), "-S2")
    )
  )
