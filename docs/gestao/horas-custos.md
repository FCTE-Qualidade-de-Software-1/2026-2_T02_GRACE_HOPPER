# Horas, Custos e Esforço (Critério AG-C5)

Esta página consolida a gestão financeira e de esforço humano da equipe **Grace Hopper** segundo a categoria **Recursos e Custos** do **PSM/CID** e o critério **AG-C5 (Transparência da Contribuição Individual)**.

Para consultar a apuração automatizada extraída diretamente das issues do GitHub (`VEC`), acesse o [Painel de Indicadores PSM/CID](../indicadores_psm.md#2-recursos-e-custos-vec).

---

## 1. Memória de Cálculo do Valor da Hora (`R$ 50,00/h`)

A equipe definiu o valor de referência de **`R$ 50,00` por hora técnica** com base no custo operacional de um analista de qualidade de software júnior / bolsista de pesquisa e desenvolvimento em engenharia de software no mercado de Brasília (DF), contemplando remuneração direta e encargos operacionais de infraestrutura.

**Tabela 1 — Composição do valor da hora técnica adotado no projeto**

| Componente de Custo | Valor de Referência | Justificativa / Base de Cálculo |
| :--- | :---: | :--- |
| Remuneração base mensal (80h mensais — dedicação parcial de 20h/semana) | `R$ 2.800,00` | Faixa de referência para analista de qualidade júnior / pesquisador em projetos de P&D universitários (UnB/Finatec). |
| Encargos trabalhistas, provisões e custos indiretos de infraestrutura (~42,8%) | `R$ 1.200,00` | Energia, licenças, depreciação de estação de trabalho local (execução de containers Docker) e conectividade. |
| **Custo mensal consolidado (base 80h/mês)** | **`R$ 4.000,00`** | Soma da remuneração direta e custos indiretos de bancada. |
| **Valor da hora técnica ($C_h$)** | **`R$ 50,00 / h`** | $\text{R\$ } 4.000,00 \div 80\text{ h/mês} = \text{R\$ } 50,00/\text{h}$. |

*Fonte: Elaborado pelos autores para padronização orçamentária do PSM/CID.*

---

## 2. Resumo Global: Estimado vs. Realizado

**Tabela 2 — Síntese orçamentária por entrega do projeto**

| Etapa / Entrega | Horas Planejadas (Linha de Base) | Custo Planejado | Horas Realizadas (Consolidadas) | Custo Realizado | Situação |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Entrega 1 (Ponto de Controle 1 — `v1.0.0-pc1`)** | `72,0 h` | `R$ 3.600,00` | `72,0 h` | `R$ 3.600,00` | Concluída (`19/19` issues fechadas) |
| **Entrega 2 (Ponto de Controle 2 — `v2.0.0-pc2`)** | `72,0 h` | `R$ 3.600,00` | **`54,0 h`** (`42,0 h` em `8` issues concluídas + `12,0 h` em `2` issues no PR `#55`) | **`R$ 2.700,00`** (`R$ 2.100,00` concluídos + `R$ 600,00` no PR `#55`) | Em fechamento (`10/13` issues executadas; `#41`, `#42` e `#48` em aberto = `18,0 h` / `R$ 900,00`) |
| **TOTAL DO PROJETO (E1 + E2)** | **`144,0 h`** | **`R$ 7.200,00`** | **`126,0 h`** (`114,0 h` concluídas + `12,0 h` no PR `#55`) | **`R$ 6.300,00`** (`R$ 5.700,00` concluídos + `R$ 600,00` no PR `#55`) | Auditoria PSM/CID reconciliada |

*Fonte: Elaborado pelos autores a partir dos registros de issues e Pull Requests no GitHub.*

---

## 3. Entrega 1 (Ponto de Controle 1) — Esforço e Custo por Integrante

A Tabela 3 apresenta a distribuição nominal de esforço, responsabilidades e custos na Entrega 1. Os centésimos da coluna de percentual foram ajustados ($4 \times 16,67\% + 2 \times 16,66\%$) para que a soma feche exatamente em **100,00%**.

**Tabela 3 — Alocação de papéis, esforço e custos individuais no Ponto de Controle 1 (Entrega 1)**

| Integrante | Matrícula UnB | Usuário GitHub | Papel Principal e Entregas no PC1 | Horas (h) | Valor / Hora | Custo Total | % Esforço |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | `23/2036770` | `@ArthurDevWorks` | Gestor de Configuração / GitPage · Automação CI/CD, plano de testes, Docker, TCLE e limiares (Issues #01, #09, #10, #11, #12, #15, #16, #18) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Fábio Santos Araujo** | `22/2022082` | `@fabiofonteles1` | Redação do Artigo (IEEE/Overleaf) e Apresentação de Slides do PC1 (Issues #13, #14, #18) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gabriel Barbaceli** | `21/1045122` | `@Nibaacriba` | Especificação GQM de Compatibilidade e Capacidade de Interação; propósito e priorização (Issues #05, #08, #17, #19) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gustavo Silva Rodrigues** | `23/2036887` | `@g-srodrigues` | Analista de Qualidade · Adaptação do modelo ISO/IEC 25010:2023, escopo e coautoria do artigo (Issues #04, #13) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | `23/2037937` | `@ItaloSamP` | Analista do Produto e Stakeholders · Arquitetura do i-Educar, ODS 4/16 e GQM de Confiabilidade e Manutenibilidade (Issues #02, #03, #06, #07) | `12h` | R$ 50,00 | R$ 600,00 | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409` | `@ChickRicks` | Revisão técnica cruzada da GitPage e validação do artigo frente às rubricas da disciplina | `12h` | R$ 50,00 | R$ 600,00 | **16,66%** |
| **TOTAL CONSOLIDADO (E1)** | — | — | **Entregáveis Consolidados — Ponto de Controle 1** | **`72h`** | **R$ 50,00/h** | **`R$ 3.600,00`** | **`100%`** |

*Fonte: Elaborado pelos autores conforme diretrizes da disciplina FGA0315 e modelo PSM/CID.*

---

## 4. Entrega 2 (Ponto de Controle 2) — Orçamento Planejado e Apuração Real por Trilha

Para a Entrega 2, foram estruturadas **12 issues originais de 6 horas cada (`#38` a `#49`, totalizando `72h` e `R$ 3.600,00`)** acrescidas da **Issue `#56` (Ação de Melhoria sobre `getSituacaoNotas`)**, distribuídas entre os 6 integrantes da equipe nos Milestones `M5` e `M6`. A Tabela 4 consolida o orçamento planejado ($4 \times 16,67\% + 2 \times 16,66\% = 100\%$) e as horas efetivamente realizadas e auditadas para a Entrega 2 (`v2.0.0-pc2`).

**Tabela 4 — Alocação planejada e realizada de esforço e custos no Ponto de Controle 2 (Entrega 2)**

| Integrante | Matrícula UnB | Usuário GitHub | Entregas Executadas / Atribuídas na Entrega 2 (Fases 4 e 5) | Issues no GitHub | Horas Planejadas | Horas Realizadas (Apontadas) | Valor / Hora | Custo Planejado (Realizado) | % Esforço Planejado |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | `23/2036770` | `@ArthurDevWorks` | Arquitetura e Testabilidade (`M8`, `M9`, `M11`) e Proteção de Interação (`Gate M12`, `M13` — PR #55 em revisão) | [#44](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/44), [#45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45) | `12h` | `12,0h`* (`6h + 6h` em PR #55) | R$ 50,00 | R$ 600,00 (`R$ 600,00`*) | **16,67%** |
| **Fábio Santos Araujo** | `22/2022082` | `@fabiofonteles1` | Agregação Multicritério (`IQC`, `IQM`), Parecer Técnico Fase 5, Slides PC2, Auditoria PSM/CID e Prep. Release E2 (PR #58) | [#47](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/47), [#49](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/49) | `12h` | `12,0h` (`6h + 6h`) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,67%** |
| **Gabriel Barbaceli** | `21/1045122` | `@Nibaacriba` | Motor Estático AST (`M7a`, `M7b`, `M10`), Renormalização de Uso (`M14`/`M15` — PR #53) e Ação de Melhoria (`getSituacaoNotas` — PR #57) | [#43](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/43), [#46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46), [#56](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/56) | `12h` | `12,0h` (`6h + 2h + 4h`) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,67%** |
| **Gustavo Silva Rodrigues** | `23/2036887` | `@g-srodrigues` | Oráculo Pedagógico Determinístico (`Gate M3 — DCNM = 100%` — PR #54) e Consolidação do Artigo v2 | [#40](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/40), [#48](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/48) | `12h` | `6,0h` (`#40` concluída; `#48` em andamento) | R$ 50,00 | R$ 600,00 (`R$ 300,00`) | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | `23/2037937` | `@ItaloSamP` | Provisionamento Docker, Coexistência (`M1 — TINCR = 100%`) e Contratos REST (`M2 — CEI = 90%` — PR #52) | [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/38), [#39](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/39) | `12h` | `12,0h` (`6h + 6h`) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409` | `@ChickRicks` | Trilha de Atomicidade Transacional (`Gate M4 — ITAE`), Triagem `M5` e Backup/Restauração (`M6 — CVPB`) | [#41](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/41), [#42](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/42) | `12h` | `0,0h` (`#41` e `#42` não concluídas no corte) | R$ 50,00 | R$ 600,00 (`R$ 0,00`) | **16,66%** |
| **TOTAL CONSOLIDADO (E2)** | — | — | **13 Issues Mapeadas — Fases 4 e 5 ISO/IEC 25040:2024** | `#38` a `#49` e `#56` | **`72h`** | **`54,0h` (`42h` concl. + `*12h` PR #55)** | **R$ 50,00/h** | **`R$ 3.600,00` (`R$ 2.700,00`)** | **`100%`** |

*Fonte: Elaborado pelos autores com base nos registros auditáveis das issues e Pull Requests no GitHub.*

---

## 5. Governança no Apontamento de Horas (Conferência GitHub vs. Linha de Base)

O controle orçamentário da equipe consolida as horas e custos por issue e por integrante nas tabelas acima:

1. **Reconciliação integral da Entrega 1 (`#01` a `#19`):** Todas as 19 issues fechadas da Entrega 1 totalizam `72,0 h` planejadas e `72,0 h` realizadas (`R$ 3.600,00`), com os campos estruturados preenchidos diretamente no GitHub.
2. **Auditoria da Entrega 2 (`#38` a `#49` e `#56`):** Das 13 issues mapeadas na Entrega 2 (orçamento planejado de `72,0 h` / `R$ 3.600,00`), **10 issues foram executadas totalizando `54,0 h` (`R$ 2.700,00`)** — sendo `42,0 h` (`R$ 2.100,00`) nas 8 issues concluídas (`#38`, `#39`, `#40`, `#43`, `#46` e `#56` já integradas na `main` = `30,0 h`, mais `#47` e `#49` no PR `#58` = `12,0 h`) e `*12,0 h` (`R$ 600,00`) nas 2 issues submetidas e em revisão no PR `#55` (`#44` e `#45`). No caso de `@Nibaacriba`, a economia de `4,0 h` na Issue `#46` (encerrada com `2,0 h` após acionamento da regra pré-declarada da Seção 3.4) foi integralmente realocada para a Issue `#56` (`4,0 h` na refatoração de `getSituacaoNotas`), mantendo sua carga total em exatas `12,0 h` (`R$ 600,00`). Restam `18,0 h` (`R$ 900,00`) nas 3 issues abertas (`#41`, `#42` e `#48`). No acumulado do projeto (E1 + E2), foram executadas `126,0 h` (`R$ 6.300,00`) frente às `144,0 h` (`R$ 7.200,00`) planejadas.
