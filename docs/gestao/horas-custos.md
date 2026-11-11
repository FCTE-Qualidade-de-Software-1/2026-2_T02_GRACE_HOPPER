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
| **Entrega 1 (Ponto de Controle 1 — `v1.0.0-pc1`)** | `72,0 h` | `R$ 3.600,00` | `72,0 h` *(55,0 h apontadas via tags de issue)* | `R$ 3.600,00` | Concluída (`19/19` issues) |
| **Entrega 2 (Ponto de Controle 2 — `v2.0.0-pc2`)** | `72,0 h` | `R$ 3.600,00` | *Em execução* | *Em apuração* | Em andamento (`12` issues abertas) |
| **TOTAL DO PROJETO (E1 + E2)** | **`144,0 h`** | **`R$ 7.200,00`** | **`72,0 h` acumuladas** | **`R$ 3.600,00` acumulados** | — |

*Fonte: Elaborado pelos autores.*

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

## 4. Entrega 2 (Ponto de Controle 2) — Orçamento Planejado por Trilha

Para a Entrega 2, foram estruturadas **12 issues de 6 horas cada (`#38` a `#49`)** divididas em **6 trilhas de especialidade** (Milestones `M5` e `M6`).

**Tabela 4 — Alocação planejada de esforço e custos para o Ponto de Controle 2 (Entrega 2)**

| Integrante | Usuário GitHub | Trilha de Especialidade (E2) | Issues Atribuídas | Horas Planejadas | Valor / Hora | Custo Planejado | % Esforço |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | `@ArthurDevWorks` | **Trilha A:** Infraestrutura Docker, Coexistência (`M1`) e Backup (`M6`) | [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/38), [#42](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/42) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gabriel Barbaceli** | `@Nibaacriba` | **Trilha B:** Interoperabilidade REST (`M2`) e Proteção de Interação (`M12`, `M13`) | [#39](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/39), [#45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gustavo Silva Rodrigues** | `@g-srodrigues` | **Trilha C:** Confiabilidade, Oráculo Pedagógico (`M3`) e Transações (`M4`, `M5`) | [#40](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/40), [#41](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/41) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | `@ItaloSamP` | **Trilha D:** Análise Estática (`M7`–`M10`) e Testabilidade (`M11`) | [#43](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/43), [#44](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/44) | `12h` | R$ 50,00 | R$ 600,00 | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `@ChickRicks` | **Trilha E:** Qualidade em Uso (`M14`, `M15`) e Julgamento Multicritério (`IQM`) | [#46](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/46), [#47](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/47) | `12h` | R$ 50,00 | R$ 600,00 | **16,66%** |
| **Fábio Santos Araujo** | `@fabiofonteles1` | **Trilha F:** Redação Científica Final (Artigo v2), Auditoria e Release E2 | [#48](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/48), [#49](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/49) | `12h` | R$ 50,00 | R$ 600,00 | **16,67%** |
| **TOTAL PLANEJADO (E2)** | — | **12 Novas Issues — Fases 4 e 5 ISO/IEC 25040:2024** | `#38` a `#49` | **`72h`** | **R$ 50,00/h** | **`R$ 3.600,00`** | **`100%`** |

*Fonte: Elaborado pelos autores.*

---

## 5. Governança no Apontamento de Horas (Conferência GitHub vs. Linha de Base)

O coletor automático `scripts/psm/coletar_dados.py` lê os campos `Horas Planejadas / Estimadas` e `Esforço Efetivo Realizado` diretamente no texto ou comentários de cada issue no GitHub:

1. **Situação observada na Entrega 1:** Das 19 issues concluídas, 14 issues tinham ambos os campos preenchidos em formato numérico estruturado no GitHub (somando `55,0 h` estimadas e `55,0 h` realizadas), enquanto as issues `#09`, `#10`, `#11`, `#12` e `#14` tiveram suas horas consolidadas na documentação da equipe, mas permaneciam com o placeholder de template no corpo da issue no GitHub.
2. **Regra para a Entrega 2:** Ao concluir cada uma das issues `#38` a `#49`, o integrante responsável deve registrar no corpo ou em comentário de fechamento da issue a linha `- **Esforço Efetivo Realizado**: X,Xh` com o tempo real cronometrado, permitindo que o cálculo automático de `VEC` capture desvios reais de esforço.
