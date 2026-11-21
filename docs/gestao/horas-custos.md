# Horas, Custos e Esforço (Critério AG-C5)

Esta página consolida a gestão financeira e de esforço humano da equipe **Grace Hopper** segundo a categoria **Recursos e Custos** do **PSM/CID** e o critério **AG-C5 (Transparência da Contribuição Individual)**.

Para consultar a apuração automatizada com gráficos interativos em SVG extraídos diretamente do GitHub (`VEC`), acesse o [Painel de Indicadores PSM/CID](../indicadores_psm.md#2-recursos-e-custos-vec).

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
| **Entrega 2 (Ponto de Controle 2 e versão final)** | `72,0 h` | `R$ 3.600,00` | **`72,0 h`** (em `13` issues executadas) | **`R$ 3.600,00`** | Concluída (`13/13` issues executadas; `#48` concluída em 21/11/2026 pelo PR #62) |
| **TOTAL DO PROJETO (E1 + E2)** | **`144,0 h`** | **`R$ 7.200,00`** | **`144,0 h`** | **`R$ 7.200,00`** | Auditoria PSM/CID reconciliada em 21/11/2026 |
*Fonte: Elaborado pelos autores a partir dos registros de issues e Pull Requests no GitHub.*

---

## 3. Matriz Consolidada de Contribuição dos Participantes

Em conformidade com o critério **AG-C5**, a Tabela 3 consolida a atuação dos 6 integrantes sob múltiplos vetores de evidência objetiva: **Commits** no histórico do Git/GitHub, **Abertura e Integração de Pull Requests**, **Issues Atribuídas e Concluídas**, **Horas Apontadas via GitHub** e **Horas Efetivamente Consolidadas** na Entrega 1.

**Tabela 3 — Matriz multidimensional de contribuição individual dos participantes**

| Integrante | Matrícula UnB | Usuário GitHub | Papel Técnico Principal | Commits | PRs Abertos | PRs Integrados | Issues Fechadas | Horas em Issues | Horas Consolidadas (E1) | % Esforço Consolidado |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | `23/2036770` | [`@ArthurDevWorks`](https://github.com/ArthurDevWorks) | Gestão de Configuração, CI/CD, Docker, Testes e GitPage | 27 | 6 | 6 | 8 | 19,0 h | **12,0 h** | **16,67%** |
| **Fábio Santos Araujo** | `22/2022082` | [`@fabiofonteles1`](https://github.com/fabiofonteles1) | Redação Científica do Artigo (Overleaf/IEEE) e Slides PC1 | 6 | 3 | 3 | 2 | 4,0 h | **12,0 h** | **16,67%** |
| **Gabriel Barbaceli** | `21/1045122` | [`@Nibaacriba`](https://github.com/Nibaacriba) | GQM de Compatibilidade e Interação; Propósito e Escopo | 9 | 8 | 8 | 4 | 12,0 h | **12,0 h** | **16,67%** |
| **Gustavo Silva Rodrigues** | `23/2036887` | [`@g-srodrigues`](https://github.com/g-srodrigues) | Analista de Qualidade, ISO/IEC 25010 e Coautoria do Artigo | 13 | 3 | 3 | 2 | 8,0 h | **12,0 h** | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | `23/2037937` | [`@ItaloSamP`](https://github.com/ItaloSamP) | Arquitetura, Stakeholders e GQM Confiabilidade/Manutenibilidade | 13 | 3 | 3 | 4 | 28,0 h | **12,0 h** | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409` | [`@ChickRicks`](https://github.com/ChickRicks) | Revisão Técnica Cruzada da GitPage e Validação das Rubricas | 0 | 0 | 0 | 0 | 0,0 h | **12,0 h** | **16,66%** |
| **TOTAL CONSOLIDADO (E1)** | — | — | **Equipe Grace Hopper — Ponto de Controle 1** | **68** | **23** | **23** | **19** | **71,0 h** | **`72,0 h`** | **`100,0%`** |

*Fonte: Dados de commits extraídos via git shortlog e API pública do GitHub; PRs e issues extraídos por scripts/psm/coletar_dados.py.*

---

## 4. Levantamento Orçamentário: Custo Inicial Orçado vs. Esforço De Fato Empregado

A metodologia do **PSM/CID** exige a comparação contínua entre a **linha de base orçamentária planejada no início do ciclo** e o **esforço financeiro efetivamente incorrido**.

A Tabela 4 detalha essa correlação por integrante, confrontando:
1. **Custo Planejado Inicial:** Linha de base simétrica de 12 horas por membro ($12\text{ h} \times \text{R\$ } 50,00/\text{h} = \text{R\$ } 600,00$ por integrante na Entrega 1);
2. **Custo Apurado via Issues:** Valor monetário das horas registradas com tags numéricas nas issues concluídas da Entrega 1;
3. **Custo Consolidado Efetivo:** Valor do esforço total incorrido (contemplando atividades extracódigo, redação do artigo no Overleaf, atas e homologações de rubrica).

**Tabela 4 — Comparativo analítico entre custo orçado no início e esforço de fato empregado**

| Integrante | Custo Planejado Inicial | Custo Apurado via Issues | Custo Consolidado E1 | Desvio Frente à Linha de Base | Interpretação da Alocação de Esforço |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Arthur Soares Parente** | R$ 600,00 | R$ 950,00 *(19,0h)* | R$ 600,00 | + R$ 350,00 *(nas issues)* | Alta concentração em infraestrutura, pipelines CI/CD de build estrito, automação Docker e scripts de suporte da GitPage. |
| **Fábio Santos Araujo** | R$ 600,00 | R$ 200,00 *(4,0h)* | R$ 600,00 | R$ 0,00 *(consolidado)* | Dedicação predominante em redação acadêmica (Overleaf/LaTeX), formatação IEEE e slides da apresentação PC1 (não pontuados em commits git). |
| **Gabriel Barbaceli** | R$ 600,00 | R$ 600,00 *(12,0h)* | R$ 600,00 | R$ 0,00 *(aderência 100%)* | Aderência exata entre horas estimadas, apontamento em issues e esforço despendido em GQM e abertura de 8 PRs. |
| **Gustavo Silva Rodrigues** | R$ 600,00 | R$ 400,00 *(8,0h)* | R$ 600,00 | R$ 0,00 *(consolidado)* | Foco dividido entre modelagem formal dos requisitos ISO/IEC 25010 no repositório e coautoria/revisão textual do artigo científico. |
| **Ítalo Alves Sampaio de Oliveira** | R$ 600,00 | R$ 1.400,00 *(28,0h)* | R$ 600,00 | + R$ 800,00 *(nas issues)* | Esforço intensivo de engenharia reversa arquitetural do i-Educar 2.12 e detalhamento rigoroso de 4 metas GQM em confiabilidade e manutenibilidade. |
| **Ricardo Lucas Winchello Vieira Branco** | R$ 600,00 | R$ 0,00 *(em issues)* | R$ 600,00 | R$ 0,00 *(consolidado)* | Atuação dedicada como revisor técnico e auditor de qualidade externa, inspecionando a GitPage e confrontando entregáveis contra as rubricas da disciplina. |
| **TOTAL DO PROJETO (E1)** | **`R$ 3.600,00`** | **`R$ 3.550,00`** | **`R$ 3.600,00`** | **R$ 0,00 consolidado** | **Orçamento 100% cumprido e aderente ao teto orçamentário da Entrega 1.** |

*Fonte: Elaborado pelos autores a partir dos dados do repositório e do Plano de Medição PSM.*

**Diferença entre as horas em issues e a consolidação da E1.** As horas registradas nas issues da Entrega 1 não cobrem as 12h consolidadas de todos os integrantes: Gustavo tem 8h registradas (`#4` e `#13`, 4h faltantes), Fábio tem 4h (`#13`, 8h faltantes) e Ricardo não tem issue com horas (12h faltantes); Arthur (19h) e Ítalo (28h) registraram mais que 12h. A `#13` tem dois responsáveis (Fábio e Gustavo), e suas 4h aparecem na linha de cada um. As horas sem issue correspondem a atividades feitas fora do GitHub (redação no Overleaf, slides e revisão) e ficaram registradas apenas na consolidação de 12h por integrante aprovada pela equipe. Por isso, o [Painel PSM/CID](../indicadores_psm.md) e o Apêndice A do artigo usam as 12h consolidadas da E1 e somam as horas das issues da E2.

### Análise Qualitativa dos Desvios e Complementaridade Técnica

A análise cruzada das Tabelas 3 e 4 evidencia a dinâmica cooperativa e complementar da equipe:
- **Trabalho Direto no Repositório (Código e Documentação Markdown):** Os integrantes Arthur, Ítalo e Gustavo concentraram maior volume de commits (53 commits somados) e horas técnicas registradas em issues, absorvendo a complexidade técnica de Docker, pipelines e modelagem arquitetural.
- **Trabalho Técnico Extracódigo (Redação Científica e Auditoria de Qualidade):** Os integrantes Fábio e Ricardo desempenharam papéis essenciais que não geram commits diretos no GitHub — respectivamente a escrita e diagramação do artigo científico de 8 páginas no Overleaf e a auditoria sistemática de conformidade das entregas frente às rubricas de avaliação da disciplina.
- **Equilíbrio Orçamentário Global:** O total acumulado apontado via issues ($71,0\text{ h} \times \text{R\$ } 50,00 = \text{R\$ } 3.550,00$) converge com precisão cirúrgica para a linha de base nominal de **R$ 3.600,00 (72,0 h)**, apresentando desvio residual inferior a 1,4%, plenamente compatível com os limites de controle estatístico do PSM.

---

## 5. Entrega 2 (Ponto de Controle 2) — Orçamento Planejado e Apuração Real por Trilha

Para a Entrega 2, foram estruturadas **12 issues originais de 6 horas cada (`#38` a `#49`, totalizando `72h` e `R$ 3.600,00`)** acrescidas da **Issue `#56` (Ação de Melhoria sobre `getSituacaoNotas`)**, distribuídas entre os 6 integrantes da equipe nos Milestones `M5` e `M6`. A Tabela 5 consolida o orçamento planejado ($4 \times 16,67\% + 2 \times 16,66\% = 100\%$) e as horas efetivamente realizadas e auditadas para a Entrega 2 (`v2.0.0-pc2`).

**Tabela 5 — Alocação planejada e realizada de esforço e custos no Ponto de Controle 2 (Entrega 2)**

| Integrante | Matrícula UnB | Usuário GitHub | Entregas Executadas / Atribuídas na Entrega 2 (Fases 4 e 5) | Issues no GitHub | Horas Planejadas | Horas Realizadas (Apontadas) | Valor / Hora | Custo Planejado (Realizado) | % Esforço Planejado |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | `23/2036770` | `@ArthurDevWorks` | Arquitetura e Testabilidade (`M8`, `M9`, `M11`) e Proteção de Interação (`Gate M12`, `M13` — PR #55) | [#44](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/44), [#45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45) | `12h` | `12,0h` (`6h + 6h`, PR #55) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,67%** |
| **Fábio Santos Araujo** | `22/2022082` | `@fabiofonteles1` | Agregação Multicritério (`IQC`, `IQM`), Parecer Técnico Fase 5, Slides PC2, Auditoria PSM/CID e Prep. Release E2 (PR #58) | [#47](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/47), [#49](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/49) | `12h` | `12,0h` (`6h + 6h`) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,67%** |
| **Gabriel Barbaceli** | `21/1045122` | `@Nibaacriba` | Motor Estático AST (`M7a`, `M7b`, `M10`), Renormalização de Uso (`M14`/`M15` — PR #53) e Ação de Melhoria (`getSituacaoNotas` — PR #57) | [#43](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/43), [#46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46), [#56](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/56) | `12h` | `12,0h` (`6h + 2h + 4h`) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,67%** |
| **Gustavo Silva Rodrigues** | `23/2036887` | `@g-srodrigues` | Oráculo Pedagógico Determinístico (`Gate M3 — DCNM = 100%` — PR #54) e Consolidação do Artigo v2 | [#40](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/40), [#48](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/48) | `12h` | `12,0h` (`6h + 6h`; `#48` concluída em 21/11) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | `23/2037937` | `@ItaloSamP` | Provisionamento Docker, Coexistência (`M1 — TINCR = 100%`) e Contratos REST (`M2 — CEI = 90%` — PR #52) | [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/38), [#39](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/39) | `12h` | `12,0h` (`6h + 6h`) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409` | `@ChickRicks` | Trilha de Atomicidade Transacional (`Gate M4 — ITAE`), Triagem `M5` e Backup/Restauração (`M6 — CVPB`) | [#41](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/41), [#42](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/42) | `12h` | `12,0h` (`6h + 6h`, PRs #59 e #61) | R$ 50,00 | R$ 600,00 (`R$ 600,00`) | **16,66%** |
| **TOTAL CONSOLIDADO (E2)** | — | — | **13 Issues Mapeadas — Fases 4 e 5 ISO/IEC 25040:2024** | `#38` a `#49` e `#56` | **`72h`** | **`72,0h` (13 issues executadas)** | **R$ 50,00/h** | **`R$ 3.600,00` (`R$ 3.600,00`)** | **`100%`** |


*Fonte: Elaborado pelos autores com base nos registros auditáveis das issues e Pull Requests no GitHub.*

---

## 6. Governança no Apontamento de Horas (Conferência GitHub vs. Linha de Base)

O controle orçamentário da equipe consolida as horas e custos por issue e por integrante nas tabelas acima:

1. **Reconciliação integral da Entrega 1 (`#01` a `#19`):** Todas as 19 issues fechadas da Entrega 1 totalizam `72,0 h` planejadas e `72,0 h` realizadas (`R$ 3.600,00`), com os campos estruturados preenchidos diretamente no GitHub.
2. **Auditoria da Entrega 2 (`#38` a `#49` e `#56`):** Das 13 issues mapeadas na Entrega 2 (orçamento planejado de `72,0 h` / `R$ 3.600,00`), **as 13 issues foram executadas, totalizando `72,0 h` (`R$ 3.600,00`)**: `#38` a `#49` e `#56`. No caso de `@Nibaacriba`, a economia de `4,0 h` na Issue `#46` (encerrada com `2,0 h` após acionamento da regra pré-declarada da Seção 3.4) foi integralmente realocada para a Issue `#56` (`4,0 h` na refatoração de `getSituacaoNotas`), mantendo sua carga total em exatas `12,0 h` (`R$ 600,00`). A issue `#48` (artigo v2) foi concluída em 21/11/2026 com `6,0 h` (`R$ 300,00`), pelo PR #62. No acumulado do projeto (E1 + E2), foram executadas `144,0 h` (`R$ 7.200,00`), iguais às planejadas.
