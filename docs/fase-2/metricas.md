# Catálogo de Métricas e Gates Binários

Esta página consolida as **15 famílias de métricas (`M1` a `M15`)**, desdobradas em **17 linhas operacionais**, com suas fórmulas matemáticas, escalas, métodos de coleta e classificação entre **Gates Binários Eliminatórios** e **Métricas Graduais**.

Para ver as definições completas linha a linha e demonstrações algébricas adicionais, consulte também o documento de referência [Especificação Completa do Framework GQM](../gqm_evaluation_framework.md).

---

## 1. Os 3 Gates Binários Eliminatórios (Não-Compensatórios)

Determinadas propriedades de um sistema de gestão escolar não admitem compensação por média: um software não pode ser aprovado se arredondar notas errado, corromper o banco em caso de falha ou aceitar notas inválidas. Por isso, **3 métricas atuam como Gates Binários** (exigem $100\%$ de conformidade):

**Tabela 1 — Especificação dos 3 Gates Binários eliminatórios da avaliação**

| Gate | Sigla e Nome da Métrica | Fórmula Matemática | Regra Eliminatória de Julgamento |
| :---: | :--- | :---: | :--- |
| **`Gate M3`** | **DCNM** — Determinismo no Cálculo de Notas e Menções | $$\text{DCNM} = \left( \frac{N_{\text{casos conformes ao oráculo}}}{N_{\text{casos de teste no manifesto}}} \right) \times 100\%$$ | **Aprovado:** $\text{DCNM} = 100\%$ (com $N_{\text{manifesto}} > 0$).<br>**Bloqueado:** $\text{DCNM} < 100\%$ classifica a release na **Classe C**. |
| **`Gate M4`** | **ITAE** — Integridade Transacional em Operações de Escrita | $$\text{ITAE} = \left( \frac{N_{\text{operações com rollback íntegro}}}{N_{\text{operações compostas testadas}}} \right) \times 100\%$$ | **Aprovado:** $\text{ITAE} = 100\%$ (zero tuplas órfãs após injeção de exceção).<br>**Bloqueado:** $\text{ITAE} < 100\%$ classifica a release na **Classe C**. |
| **`Gate M12`** | **IPPE** — Índice de Prevenção e Proteção contra Erros do Usuário | $$\text{IPPE} = \left( \frac{N_{\text{entradas inválidas bloqueadas com segurança}}}{N_{\text{cenários inválidos submetidos}}} \right) \times 100\%$$ | **Aprovado:** $\text{IPPE} = 100\%$ (em $\ge 12$ cenários inválidos, sem erro 500 ou gravação).<br>**Bloqueado:** $\text{IPPE} < 100\%$ classifica a release na **Classe C**. |

*Fonte: Elaborado pelos autores.*

---

## 2. Catálogo Completo das 17 Linhas Operacionais (`M1` a `M15`)

### 2.1 Compatibilidade (`G1` — Peso Global: 20%)

**Tabela 2 — Métricas de Compatibilidade (`M1` e `M2`)**

| Linha | Subcaracterística | Nome e Sigla | Equação de Cálculo | Unidade / Escala | Instrumento de Coleta |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **`M1`** | Coexistência | **TINCR** — Taxa de Isolamento e Não-Colisão de Recursos | $$\text{TINCR} = \left(\frac{N_{\text{recursos isoláveis sem colisão}}}{N_{\text{recursos compartilháveis identificados}}}\right) \times 100\%$$ | `%` (Razão) | Inspeção de `docker-compose.yml` e `.env` + subida simultânea de 2ª instância. |
| **`M2`** | Interoperabilidade | **CEI** — Conformidade de Esquema de Interoperabilidade | $$\text{CEI} = \left(\frac{N_{\text{endpoints conformes aos 3 critérios}}}{N_{\text{endpoints avaliados}}}\right) \times 100\%$$ | `%` (Razão) | Bateria de testes de contrato JSON Schema sobre endpoints REST de Matrícula e Diário. |

---

### 2.2 Confiabilidade (`G2` — Peso Global: 30%)

**Tabela 3 — Métricas de Confiabilidade (`M3` a `M6`)**

| Linha | Subcaracterística | Nome e Sigla | Equação de Cálculo | Unidade / Escala | Instrumento de Coleta |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **`M3`** | Ausência de Falhas | **DCNM** — Determinismo no Cálculo de Notas e Menções | $$\text{DCNM} = \left(\frac{N_{\text{casos conformes}}}{N_{\text{casos do oráculo}}}\right) \times 100\%$$ | `%` (**Gate Binário**) | Suíte automatizada Pest/PHPUnit sobre `Avaliacao_Service_Boletim` e regras de arredondamento. |
| **`M4`** | Tolerância a Falhas | **ITAE** — Integridade Transacional em Operações de Escrita | $$\text{ITAE} = \left(\frac{N_{\text{rollbacks íntegros}}}{N_{\text{escritas compostas testadas}}}\right) \times 100\%$$ | `%` (**Gate Binário**) | Injeção controlada de exceção em `RegistrationService` e `Boletim` + auditoria SQL no PostgreSQL. |
| **`M5`** | Ausência de Falhas | **DDOM** — Densidade de Defeitos em Operações de Matrícula | $$\text{DDOM} = \frac{N_{\text{incidentes confirmados (90d)}}}{N_{\text{movimentações de matrícula (90d)}}} \times 1000$$ | `defeitos / 1000 mov.` | Logs operacionais de 90 dias *(declarada não mensurável em ambiente sem produção; ver regra de renormalização)*. |
| **`M6`** | Recuperabilidade | **CVPB** — Completude de Verificação de Backup | $$\text{CVPB} = \left(\frac{N_{\text{restaurações íntegras verificadas}}}{N_{\text{unidades de backup planejadas}}}\right) \times 100\%$$ | `%` (Razão) | Execução de `pg_dump` / `pg_restore` em banco limpo com conferência de checksum SHA-256, tuplas e FKs. |

---

### 2.3 Manutenibilidade (`G3` — Peso Global: 30%)

**Tabela 4 — Métricas de Manutenibilidade (`M7a` a `M11`)**

| Linha | Subcaracterística | Nome e Sigla | Equação de Cálculo | Unidade / Escala | Instrumento de Coleta |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **`M7a`** | Analisabilidade | **CC-P90** — Complexidade Ciclomática no Percentil 90 | $$\text{CC}_{P90} = v(G)_{(r)}, \quad r = \lceil 0{,}90 \cdot n \rceil$$ | Inteiro (Ordinal/Razão) | Motor estático `scripts/evaluate-quality.php` sobre os $n$ métodos concretos em escopo. |
| **`M7b`** | Analisabilidade | **CC-MAX** — Complexidade Ciclomática Máxima | $$\text{CC}_{\max} = \max_{m \in \{1..n\}} v(G_m)$$ | Inteiro (Absoluta) | Motor estático `scripts/evaluate-quality.php` identificando o método de maior ramificação lógica. |
| **`M8`** | Modularidade e Modificabilidade | **DSPM** — Distância Média da Sequência Principal de Martin | $$\text{DSPM} = \frac{1}{K}\sum_{p=1}^{K} |A_p + I_p - 1|$$ | $[0, 1]$ (Razão) | Análise estática de acoplamento aferente ($C_a$), eferente ($C_e$) e abstração ($A_p$) por componente. |
| **`M9`** | Modularidade e Modificabilidade | **IFDL** — Índice de Fricção de Dados Legado-Moderno | $$\text{IFDL} = \frac{1}{M}\sum_{j=1}^{M} \frac{N_{\text{adaptações},j}}{N_{\text{membros},j}}$$ | Razão adimensional | Auditoria estática de pontos lógicos de adaptação nos modelos Eloquent `app/Models/Legacy*.php`. |
| **`M10`** | Analisabilidade | **MI** — Índice de Manutenibilidade Normalizado | $$\text{MI}_m = \text{clip}_{[0,100]}\!\left(\frac{171 - 5{,}2\ln(HV_m) - 0{,}23\,v(G_m) - 16{,}2\ln(LOC_m)}{171}\times 100\right)$$ | $[0, 100]$ (Intervalar) | Extração de Volume de Halstead ($HV_m$), $v(G_m)$ e $LOC_m$ via `scripts/evaluate-quality.php`. |
| **`M11`** | Testabilidade | **TTAE** — Taxa de Testes Ativos com Asserção Efetiva | $$\text{TTAE} = \left(\frac{N_{\text{testes executados com asserção}}}{N_{\text{testes declarados no escopo}}}\right) \times 100\%$$ | `%` (Razão) | Execução do runner Pest/PHPUnit + detecção de casos ignorados com `markTestSkipped()`. |

---

### 2.4 Capacidade de Interação e Qualidade em Uso (`G4` — Peso Global: 20%)

**Tabela 5 — Métricas de Capacidade de Interação e Qualidade em Uso (`M12` a `M15`)**

| Linha | Subcaracterística | Nome e Sigla | Equação de Cálculo | Unidade / Escala | Instrumento de Coleta |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **`M12`** | Proteção contra Erros | **IPPE** — Índice de Prevenção e Proteção contra Erros | $$\text{IPPE} = \left(\frac{N_{\text{bloqueios seguros}}}{N_{\text{entradas inválidas}}}\right) \times 100\%$$ | `%` (**Gate Binário**) | Submissão de catálogo com $\ge 12$ entradas inválidas na UI e API + conferência no banco. |
| **`M13`** | Autodescritividade | **ADMV** — Autodescritividade das Mensagens de Validação | $$\text{ADMV} = \left(\frac{N_{\text{mensagens claras (causa + ação)}}}{N_{\text{mensagens avaliadas}}}\right) \times 100\%$$ | `%` (Razão) | Avaliação independente por 2 revisores sobre as mensagens de `Portabilis_Messenger` e `Error.php`. |
| **`M14a`** | Eficiência em Uso (ISO 25019) | **TMET-T1** — Razão de Tempo Médio na Tarefa `T1` (Matrícula) | $$R_{\text{tempo},T1} = \frac{\overline{\text{TMET}}_{T1}}{T_{\text{ref},T1}}$$ | Razão adimensional | Sessões cronometradas sob TCLE com $\ge 5$ iniciantes (`P01`–`P05`) vs. média de 3 execuções de referência. |
| **`M14b`** | Eficiência em Uso (ISO 25019) | **TMET-T2** — Razão de Tempo Médio na Tarefa `T2` (Diário/Notas) | $$R_{\text{tempo},T2} = \frac{\overline{\text{TMET}}_{T2}}{T_{\text{ref},T2}}$$ | Razão adimensional | Sessões cronometradas sob TCLE no lançamento de notas de turma de 10 alunos vs. $T_{\text{ref},T2}$. |
| **`M15`** | Eficácia em Uso (ISO 25019) | **TSPT** — Taxa de Sucesso na Primeira Tentativa | $$\text{TSPT} = \left(\frac{N_{\text{execuções corretas na 1ª submissão}}}{N_{\text{total de execuções (T1 + T2)}}}\right) \times 100\%$$ | `%` (Razão) | Observação direta e conferência no PostgreSQL após a 1ª submissão de cada participante. |

*Fonte: Elaborado pelos autores.*
