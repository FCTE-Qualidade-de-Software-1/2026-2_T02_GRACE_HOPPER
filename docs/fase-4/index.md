# Fases 4 e 5: Executar e Concluir a Avaliação (Entrega 2)

As **Fases 4 e 5** correspondem às Atividades 4 (*Execute the evaluation*) e 5 (*Conclude the evaluation*) da **ISO/IEC 25040:2024** e compõem o escopo da **Entrega 2 (Ponto de Controle 2 — `v2.0.0-pc2`)**.

!!! info "Status Atual da Etapa — Fases 4 e 5 Consolidadas"
    - **Situação:** Medições de `M1`, `M2`, `M3`, `M7a`, `M7b`, `M10`, declaração prévia de `M14a`, `M14b` e `M15`, Ação de Melhoria (`#56`) e Julgamento Multicritério da Fase 5 (`#47`, `#49`) consolidados; medições de `M8`, `M9`, `M11`, `M12` e `M13` submetidas no PR [#55](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pull/55) (em revisão); `M4`, `M6` e Artigo v2 (`#41`, `#42`, `#48`) em aberto.
    - **Acompanhamento ao vivo:** Consulte o progresso em tempo real no [Painel do Projeto](../painel_projeto.md) e no [Painel de Indicadores PSM/CID](../indicadores_psm.md).

---

## 1. Roteiro de Execução por Trilha (Fase 4 — Milestone `M5` e `M6`)

A execução empírica sobre o commit congelado `7903a3efc7689942ee700007f86ed581023aad27` do **i-Educar 2.12** está distribuída nas trilhas técnicas da Tabela 1:

**Tabela 1 — Cronograma operacional de coleta e julgamento para a Entrega 2**

| Trilha e Responsável | Issues | Métricas e Gates no Escopo | Status e Entregável Técnico Consolidado |
| :--- | :---: | :---: | :--- |
| **Trilha A/B — Compatibilidade (G1)**<br>*(Ítalo Alves Sampaio)* | [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/38), [#39](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/39) | `M1` (`TINCR`), `M2` (`CEI`) | **Concluída na `main` (PR #52):** duas instâncias isoladas ($\text{TINCR} = 100{,}0\%$) e contratos JSON Schema validados em 10 endpoints ($\text{CEI} = 90{,}0\%$). |
| **Trilha C/A — Confiabilidade e Oráculo (G2)**<br>*(Gustavo Silva Rodrigues / Ricardo Lucas Winchello)* | [#40](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/40), [#41](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/41), [#42](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/42) | **`Gate M3`** (`DCNM`), **`Gate M4`** (`ITAE`), `M5` (`DDOM`), `M6` (`CVPB`) | **Parcial (`#40` concluída no PR #54; `#41` concluída no PR #58; `#42` em aberto):** 30 cenários do oráculo sobre `Boletim.php` (**Gate M3 APROVADO**, $\text{DCNM} = 100{,}0\%$, 457 asserções), `M5` não mensurável por ausência de dados de produção (política prévia da Seção 3.1), `M4` REPROVADO (ITAE = 0/1 = 0%)** e **`M6` APROVADO (CVPB = 100%, S=4)**. |
| **Trilha D — Manutenibilidade e Melhoria (G3)**<br>*(Gabriel Barbaceli / Arthur Soares Parente)* | [#43](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/43), [#44](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/44), [#56](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/56) | `M7a`, `M7b`, `M8`, `M9`, `M10`, `M11` + Patch `getSituacaoNotas` | **`#43` e `#56` concluídas na `main` (PRs #53 e #57); `#44` em revisão (PR #55):** 213 callables nos 4 arquivos do manifesto ($\text{CC}_{P90} = 8$, $\text{CC}_{\max} = 72$, $\text{MI} = 63{,}82$); no patch da `#56` (221 callables), $v(G)$ de `getSituacaoNotas` cai de $72$ para $15$ e $\text{CC}_{\max}$ cai para $30$; no PR #55, $\text{DSPM} = 0{,}38$, $\text{IFDL} = 4{,}56$ e $\text{TTAE} = 78{,}92\%$. |
| **Trilha B/E — Interação e Qualidade em Uso (G4)**<br>*(Arthur Soares Parente / Gabriel Barbaceli)* | [#45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45), [#46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46) | **`Gate M12`** (`IPPE`), `M13` (`ADMV`), `M14a/b` (`TMET`), `M15` (`TSPT`) | **`#46` concluída na `main` (PR #53); `#45` em revisão (PR #55):** renormalização pré-declarada de `M14a/b` e `M15`; no PR #55, bateria de 12 cenários inválidos (**Gate M12 APROVADO**, $\text{IPPE} = 100{,}0\%$) e auditoria de mensagens ($\text{ADMV} = 75{,}00\%$, Crítico, $S_{13}=1$). |
| **Trilha E/F — Julgamento Fase 5 e PC2**<br>*(Fábio Santos Araujo)* | [#47](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/47), [#49](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/49) | Julgamento dos Gates, $\text{IQC}_k$, $\text{IQM}$, Parecer Fase 5, PC2 e Auditoria PSM/CID | **Concluída no PR #58:** julgamento estrito conforme Seção 5 do Framework GQM ($\text{IQM}$ oficial suspenso por `M4`/`M6`; análise de sensibilidade de cenários), parecer por stakeholder, slides PC2 e auditoria de horas/custos. |
| **Trilha F — Artigo Científico Final (LaTeX)**<br>*(Gustavo Silva Rodrigues)* | [#48](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/48) | Consolidação Científica IEEE (`docs/artigo/main.tex`) | **Em aberto:** consolidação das seções de Resultados, Discussão, Ameaças à Validade e Conclusão no artigo IEEE. |

*Fonte: Elaborado pelos autores.*

---

### 1.1 Relatórios Técnicos da Fase 4

- [Compatibilidade — M1 (TINCR) e M2 (CEI)](../plano_medicao_testes.md#6-resultados-da-execucao-da-caracteristica-compatibilidade-g1-issues-38-e-39): isolamento de recursos em containers e conformidade contratual de 10 endpoints REST.
- [Confiabilidade — M3 (DCNM, Gate Binário)](medicao_m3_dcnm.md): execução oficial dos 30 cenários do oráculo de notas e menções (`oficial-001`, 457 asserções).
- [Medição M4 e M5 — Atomicidade Transacional (ITAE) e Triagem DDOM](medicao_m4_itae_m5_ddom.md)
- [Manutenibilidade (M7a, M7b e M10)](manutenibilidade-m7-m10.md): resultado da execução do motor estático sobre os 213 callables dos 4 arquivos do manifesto no commit congelado.
- [Manutenibilidade (M8, M9 e M11)](manutenibilidade-m8-m9-m11.md): distância da sequência principal de Martin (M8), atrito legado-moderno (M9) e taxa de testes ativos com asserção (M11).
- [Capacidade de interação (Gate M12 e M13)](interacao-m12-m13.md): testes de proteção contra erros do usuário (Gate M12) e auditoria de autodescritividade das mensagens de validação (M13).
- [Qualidade em uso (M14a, M14b e M15)](qualidade-em-uso-m14-m15.md): métricas declaradas não mensuráveis antes da coleta e renormalização do $\text{IQC}_{\text{Interação}}$.
- [Ação de melhoria](acao-de-melhoria.md): refatoração de `getSituacaoNotas` ($v(G)$ de 72 para 15), com teste de equivalência de comportamento (50.000 cenários pseudoaleatórios, semente 2026) e nova medição de M7a, M7b e M10.
- [Consolidação de M4 a M15 na Seção 8 do Plano de Medição](../plano_medicao_testes.md#8-resultados-consolidados-das-medicoes-m4-a-m15-e-acao-de-melhoria-fase-4): síntese de G2 (`M4`, `M5`, `M6`), G3 (`M8`, `M9` e `M11` do PR [#55](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pull/55)) e G4 (`M12` e `M13` do PR [#55](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pull/55)).

---

## 2. Julgamento Multicritério e Decisão de Release (Fase 5 — Issue #47)

A consolidação completa da Atividade 5 da ISO/IEC 25040:2024 encontra-se na [Seção 9 do Plano Operacional de Medição e Testes](../plano_medicao_testes.md#9-conclusao-da-avaliacao-agregacao-multicriterio-julgamento-dos-gates-e-parecer-tecnico-fase-5-isoiec-250402024). Abaixo apresenta-se o resumo executivo dos três pilares de decisão sobre o **commit congelado `7903a3efc7689942ee700007f86ed581023aad27`**:

### 2.1 Veredito dos 3 Gates Binários Eliminatórios

1. **Gate 1 — `M3 (DCNM)`:** **APROVADO** ($\text{DCNM} = 30/30 = 100{,}0\%$, $457$ asserções em `evidencias/g2_confiabilidade/m3/oficial-001/summary.json`).
2. **Gate 2 — `M4 (ITAE)`:** **REPROVADO** (FAIL, ITAE = 0/1 = 0%) — evidência em evidencias/g2_confiabilidade/m4/rodada-001/summary.json
3. **Gate 3 — `M12 (IPPE)`:** **APROVADO (no PR #55, em revisão)** ($\text{IPPE} = 12/12 = 100{,}0\%$, zero persistência indevida e zero HTTP 500 nas capturas de `evidencias/g4_interacao_uso/capturas_m12/` e `m12_ippe.csv` do PR [#55](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pull/55)).

### 2.2 Índices de Qualidade por Característica ($\text{IQC}_k$) e Índice Global ($\text{IQM}$)

Conforme a regra da **Seção 5.2 e Figura 2 do Framework GQM**, quando uma métrica gradual fica sem dados e não existe política prévia de exclusão/renormalização (caso de `M6` — e do Gate `M4` — na característica Confiabilidade), a característica correspondente e o $\text{IQM}$ ficam **não calculáveis / suspensos**, sendo vedado atribuir nota máxima implícita às métricas ausentes. Os valores de sensibilidade (incluindo o efeito do patch da Issue `#56`) são reportados separadamente como simulação de cenários:

**Tabela 2 — Índices $\text{IQC}_k$ e $\text{IQM}$ oficiais no commit congelado (`7903a3e`) e análise de sensibilidade pós-melhoria (`#56`)**

| Dimensão Avaliada | Peso Global ($W_k$) | Valor Oficial no Commit Congelado (`7903a3e`) | Cenário de Sensibilidade Pós-Patch (`#56`) | Situação frente às Regras da Seção 5 do Framework GQM |
| :--- | :-: | :-: | :-: | :--- |
| **G1 — Compatibilidade** ($\text{IQC}_{\text{Comp}}$) | $20\%$ | **$3{,}50$** | **$3{,}50$** | Calculado e aprovado ($\ge 3{,}00$, nível de Classe A) |
| **G2 — Confiabilidade** ($\text{IQC}_{\text{Conf}}$) | $30\%$ | **$2{,}80$** | **$2{,}80$** | `M3 = 100%` ($S=4$), `M4` REPROVADO (ITAE = 0%, $S=1$), `M6 = 100%` ($S=4$, Issue `#42`); `M5` excluída pela política §3.1. |
| **G3 — Manutenibilidade** ($\text{IQC}_{\text{Manut}}$) | $30\%$ | **$2{,}20$** *(c/ PR #55)* | **$2{,}60$** *(c/ patch #56 + PR #55)* | **Reprovado no commit congelado ($2{,}20 < 2{,}50$)**; no cenário com o patch da `#56`, sobe para $2{,}60 \ge 2{,}50$ |
| **G4 — Interação e Uso** ($\text{IQC}_{\text{Interação}}$) | $20\%$ | **$3{,}14$** *(c/ PR #55)* | **$3{,}14$** *(c/ PR #55)* | Renormalizado por política prévia (`M14`/`M15` excluídas) com `M12` ($S=4$) e `M13` ($75{,}00\% \Rightarrow S=1$, Crítico) |
| **Índice Global ($\text{IQM}$)** | **$100\%$** | **$2{,}83$** | **$2{,}95$** *(c/ patch #56)* | Calculado (Gate M4 reprovado determina Classe C, mas $\text{IQM} \ge 2{,}75$) |

*Fonte: Elaborado pelos autores com base na Seção 9.3 do Plano Operacional de Medição e Testes.*

### 2.3 Classificação Final do Produto e Cenário de Transição

- **Classificação Oficial do Produto Avaliado (Commit Congelado `7903a3e`):** **CLASSE C — Reprovado / Bloqueado**, determinada pelo **Gate Binário `M4 (ITAE)` reprovado (ITAE = 0/1 = 0%)** e pelo índice $\text{IQC}_{\text{Manut}} = 2{,}20 < 2{,}50$ no código original (o $\text{IQM} = 2{,}83$ é calculável após M6, mas não eleva a classe por conta do Gate M4)
- **Cenário Hipotético de Transição para a Classe B (Análise de Sensibilidade):** Como o objeto avaliado é o commit congelado `7903a3e` (que não inclui o patch da Issue `#56`), a qualificação para a **Classe B (Aprovado com Ressalvas)** é apresentada como cenário condicionado a: (i) incorporação do patch [`getSituacaoNotas.patch`](../evidencias/melhoria/getSituacaoNotas.patch) ao repositório upstream (elevando $\text{IQC}_{\text{Manut}}$ de $2{,}20$ para $2{,}60 \ge 2{,}50$), (ii) conclusão da revisão e merge do PR [#55](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/pull/55) (`M8`, `M9`, `M11`, `M12` e `M13`) e (iii) correção de `Boletim::save()` (envolver `saveNotas()`, `saveFaltas()`, `savePareceres()` e `promover()` em `DB::transaction`) seguida de remediação do Gate `M4` ($\text{ITAE} = 100\%$) e execução de `M6` ($\text{CVPB}$). Mesmo nesse cenário, o produto permaneceria em Classe B (e não Classe A) devido à presença de métricas em nível Crítico ($S_i = 1$ em `M9` e `M13`).
- Consulte o [Plano de Ação Corretiva Priorizado (Tabela 11)](../plano_medicao_testes.md#95-plano-de-acao-corretiva-priorizado-backlog-de-engenharia) e o [Parecer Técnico por Stakeholder (Seção 9.6)](../plano_medicao_testes.md#96-parecer-tecnico-conclusivo-por-categoria-de-stakeholder-isoiec-25040-processo-53).
