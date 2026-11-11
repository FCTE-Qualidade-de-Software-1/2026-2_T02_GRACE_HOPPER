# Plano de Medição da Gestão (PSM/CID)

No modelo **PSM (*Practical Software and Systems Measurement*)**, toda medida de gestão deve responder a uma **necessidade de informação** concreta da equipe e possuir **critérios de decisão** predefinidos que orientem ações corretivas.

Cada um dos quatro indicadores adotados pela equipe **Grace Hopper** foi especificado utilizando o template formal de **Instância do Modelo de Informação (*Measurement Construct*)**, detalhando desde os atributos básicos coletados no GitHub até o modelo de análise e os limites de decisão.

- Os valores atualizados automaticamente a cada *push* estão no [Painel de Indicadores PSM/CID](../indicadores_psm.md).
- A interpretação histórica e as decisões tomadas a cada etapa constam no [Registro de Medições e Decisões](registro-de-medicoes.md).

---

## 1. Taxa de Conclusão por Milestone (`TCM`)

Originada da categoria *Schedule and Progress* ( Conceito mensurável: *Work Unit Progress* — *Committed vs. Completed*, Tabela 5, linha 1 do PSM/CID Parte 1 e seção 8.3 da Parte 2).

**Tabela 1 — Instância do modelo de informação de `TCM` (Planejado vs. Concluído por Marco)**

| Campo do Modelo de Informação | Especificação no Projeto Grace Hopper |
| :--- | :--- |
| **Necessidade de informação** | As tarefas planejadas para cada marco (milestone) estão sendo entregues? Há risco de deixar entregáveis obrigatórios incompletos no Ponto de Controle? |
| **Conceito mensurável** | Progresso das unidades de trabalho (*Work Unit Progress*) |
| **Entidades relevantes** | Issues associadas aos milestones `M0` a `M6` do repositório no GitHub |
| **Atributos** | Estado da issue (`open` ou `closed`) e vínculo com o milestone |
| **Medidas básicas** | 1. $N_{\text{planejadas}}$ = contagem de issues atribuídas ao milestone.<br>2. $N_{\text{concluídas}}$ = contagem de issues fechadas (`state = closed`) no milestone. |
| **Método de medição** | Contagem automatizada via API REST do GitHub executada por `scripts/psm/coletar_dados.py` e processada em `scripts/psm/indicadores.py`. |
| **Tipo de método de medição** | Objetivo |
| **Escala e Tipo de escala** | Números inteiros de $0$ a $\infty$ · Escala de **Razão** |
| **Unidade de medida** | Issue (unidade atômica de trabalho) |
| **Medida derivada** | Taxa de Conclusão por Milestone ($\text{TCM}$) em percentual |
| **Função de medição** | $$\text{TCM} = \frac{N_{\text{concluídas}}}{N_{\text{planejadas}}} \times 100\%$$ |
| **Indicador** | Cartão de topo e gráfico de barras horizontais por milestone no [Painel PSM/CID](../indicadores_psm.md) |
| **Modelo de análise** | $\text{TCM} = 100\%$ ao final do marco indica cumprimento integral do escopo planejado; valores inferiores indicam pendências que precisam ser redistribuídas ou replanejadas. |
| **Critérios de decisão** | **Guia PSM/CID (Parte 2, p. 17):** desvio $> 5\%$ no fim do marco requer investigação de causa; desvio $> 10\%$ exige ação corretiva.<br>**Acordo da equipe:** se $\text{TCM} < 50\%$ na metade do período do marco, redistribuir as issues abertas entre os integrantes da trilha correspondente. |

*Fonte: Elaborado pelos autores com base no PSM/CID (2021) e diretrizes da disciplina FGA0315.*

---

## 2. Aderência ao Calendário dos Marcos (`ACM`)

Complementa o monitoramento de progresso verificando a pontualidade do fechamento de cada milestone em relação à data-limite (*due date*) e o desvio temporal por issue.

**Tabela 2 — Instância do modelo de informação de `ACM` (Cumprimento de Prazo dos Marcos)**

| Campo do Modelo de Informação | Especificação no Projeto Grace Hopper |
| :--- | :--- |
| **Necessidade de informação** | Os marcos do projeto estão sendo concluídos dentro das datas-limite alinhadas às entregas da disciplina? Qual o desvio médio em dias das issues em relação ao prazo? |
| **Conceito mensurável** | Aderência ao cronograma de marcos (*Milestone Schedule Adherence*) |
| **Entidades relevantes** | Milestones (`M0` a `M6`) e respectivas issues do repositório |
| **Atributos** | Data-limite do milestone (`due_on`, considerada até 23h59 no horário de Brasília) e timestamp de fechamento da última issue (`closed_at`) |
| **Medidas básicas** | 1. $M_{\text{avaliados}}$ = quantidade de milestones com prazo definido já vencido.<br>2. $M_{\text{no prazo}}$ = quantidade de milestones cuja última issue foi fechada até $23\text{h}59$ da data `due_on`.<br>3. $\Delta d_i = t_{\text{fechamento},i} - t_{\text{prazo},m}$ = desvio em dias de cada issue $i$. |
| **Método de medição** | Leitura automática de `due_on` e `closed_at` na API do GitHub por `scripts/psm/indicadores.py` (`acm` e `desvios_prazo`). |
| **Tipo de método de medição** | Objetivo |
| **Escala e Tipo de escala** | Datas/horas (Intervalar) para timestamps; Reais em dias (Intervalar/Razão) para desvios; Percentual $[0\%, 100\%]$ (Razão) para a taxa $\text{ACM}$. |
| **Unidade de medida** | Marco concluído (%) e Dias ($\text{d}$) |
| **Medida derivada** | Aderência ao Calendário dos Marcos ($\text{ACM}$) e Desvio Médio de Prazo ($\overline{\Delta d}$) |
| **Função de medição** | $$\text{ACM} = \frac{M_{\text{no prazo}}}{M_{\text{avaliados}}} \times 100\%$$ |
| **Indicador** | Cartão `ACM`, Tabela de Situação dos Marcos e Gráfico de Desvio por Issue (Figura 2) no [Painel PSM/CID](../indicadores_psm.md) |
| **Modelo de análise** | Valores negativos de $\Delta d_i$ indicam conclusão adiantada; valores positivos ($\Delta d_i > 0$) evidenciam atraso em relação ao marco. Se `due_on` não estiver preenchido no GitHub, o indicador reporta `n/c` (não calculável). |
| **Critérios de decisão** | **Equipe:** qualquer issue aberta a menos de 48h do vencimento do milestone sem PR vinculado aciona revisão imediata pelo par da trilha; ausência de `due_on` cadastrado bloqueia a apuração de `ACM` e exige atualização da governança no GitHub. |

*Fonte: Elaborado pelos autores com base no PSM/CID (2021).*

---

## 3. Variação de Esforço e Custo (`VEC`)

Originada da categoria *Resources and Cost* (Conceito mensurável: *Financial & Effort Performance* — *Estimate vs. Actual Effort*, Tabela 5, linhas 8 e 9 do PSM/CID Parte 1).

**Tabela 3 — Instância do modelo de informação de `VEC` (Estimado vs. Realizado)**

| Campo do Modelo de Informação | Especificação no Projeto Grace Hopper |
| :--- | :--- |
| **Necessidade de informação** | As estimativas de esforço (em horas) e de custo financeiro ($R\$ 50,00/\text{h}$) definidas no planejamento são realistas frente ao esforço efetivamente despendido? |
| **Conceito mensurável** | Precisão da estimativa de esforço e desempenho de custo (*Effort & Cost Estimation Accuracy*) |
| **Entidades relevantes** | Issues concluídas do repositório que possuem registro de horas planejadas e realizadas |
| **Atributos** | Campo `Horas Planejadas / Estimadas` ($E_i$), campo `Esforço Efetivo Realizado` ($R_i$) e taxa horária padrão ($C_h = R\$ 50,00/\text{h}$) |
| **Medidas básicas** | 1. $E_{\text{planejado}} = \sum E_i$ (soma das horas estimadas nas issues concluídas com ambos os registros).<br>2. $R_{\text{realizado}} = \sum R_i$ (soma das horas efetivamente realizadas no mesmo conjunto de issues). |
| **Método de medição** | Extração via expressões regulares (`RE_ESTIMADA` e `RE_REALIZADA`) no corpo e comentários das issues por `scripts/psm/coletar_dados.py`, complementada pela tabela consolidada em [Horas e Custos](horas-custos.md). |
| **Tipo de método de medição** | 1. Subjetivo na estimativa inicial (baseada na experiência da equipe).<br>2. Objetivo na apuração das horas registradas. |
| **Escala e Tipo de escala** | Reais positivos para horas e moeda; Reais ($-100\%$ a $+\infty$) na escala de **Razão** para a variação. |
| **Unidade de medida** | Horas ($\text{h}$), Reais ($\text{R\$}$) e Percentual ($\%$) |
| **Medidas derivadas** | Variação de Esforço e Custo ($\text{VEC}$) e Custo Realizado ($C_{\text{real}} = R_{\text{realizado}} \times R\$ 50,00$) |
| **Função de medição** | $$\text{VEC} = \frac{R_{\text{realizado}} - E_{\text{planejado}}}{E_{\text{planejado}}} \times 100\%$$ |
| **Indicador** | Cartão `VEC` e Tabela de Apuração de Esforço/Custo no [Painel PSM/CID](../indicadores_psm.md) e quadros individuais em [Horas e Custos](horas-custos.md) |
| **Modelo de análise** | $\text{VEC} > 0\%$ indica subestimativa (tarefas demandaram mais tempo que o previsto); $\text{VEC} < 0\%$ indica superestimativa; $\text{VEC} = 0\%$ com todos os registros idênticos alerta para apontamento pró-forma que precisa de maior granularidade. |
| **Critérios de decisão** | **Equipe:** $|\text{VEC}| > 25\%$ (equivalente a razão $> 1,25$ ou $< 0,75$) exige recalibração das estimativas da etapa seguinte; qualquer issue fechada sem o campo `Esforço Efetivo Realizado` preenchido é listada como pendência de auditoria no painel. |

*Fonte: Elaborado pelos autores com base no PSM/CID (2021).*

---

## 4. Taxa de Revisão e Conformidade Documental (`TRCD`)

Originada da categoria *Process Performance* (Conceito mensurável: *Process Compliance and Verification Effectiveness*), monitorando a qualidade do processo de integração contínua da equipe.

**Tabela 4 — Instância do modelo de informação de `TRCD` (Conformidade de Build e Revisão de PRs)**

| Campo do Modelo de Informação | Especificação no Projeto Grace Hopper |
| :--- | :--- |
| **Necessidade de informação** | As alterações de documentação e código integradas à branch `main` cumprem o padrão de build estrito (`mkdocs build --strict` + `check_site.sh`) e passam por revisão de outro membro antes do merge? |
| **Conceito mensurável** | Efetividade da verificação e conformidade do processo (*Process Compliance*) |
| **Entidades relevantes** | Pull Requests (PRs) integrados (`merged_at != null`) no repositório |
| **Atributos** | Status de conclusão do workflow `Deploy GitHub Pages` no commit de cabeça (`head_sha`) e revisões com estado `APPROVED` emitidas por integrante distinto do autor do PR |
| **Medidas básicas** | 1. $N_{\text{PRs integrados}}$ = total de PRs com merge na `main`.<br>2. $N_{\text{PRs build OK}}$ = PRs integrados cujo workflow de validação estrita concluiu com `success`.<br>3. $N_{\text{PRs aprovados}}$ = PRs integrados com revisão `APPROVED` anterior a `merged_at`. |
| **Método de medição** | Verificação automatizada de PRs, *reviews* e *workflow runs* pela API do GitHub em `scripts/psm/coletar_dados.py` e `scripts/psm/indicadores.py`. |
| **Tipo de método de medição** | Objetivo |
| **Escala e Tipo de escala** | Percentual de $0\%$ a $100\%$ · Escala de **Razão** |
| **Unidade de medida** | Pull Request conforme ($\%$) |
| **Medida derivada** | Taxa de Revisão e Conformidade Documental ($\text{TRCD}$) e Taxa de Aprovação por Pares |
| **Função de medição** | $$\text{TRCD} = \frac{N_{\text{PRs build OK}}}{N_{\text{PRs integrados}}} \times 100\%$$ |
| **Indicador** | Cartão `TRCD`, seção Desempenho dos Processos e gráfico de evolução semanal (Figura 3) no [Painel PSM/CID](../indicadores_psm.md) |
| **Modelo de análise** | Mede a disciplina de engenharia da equipe: garante ausência de links quebrados, equações mal formatadas ou diagramas inválidos na GitPage publicada. |
| **Critérios de decisão** | **Equipe:** meta de $\text{TRCD} = 100\%$ para todos os PRs abertos após a implantação do workflow de CI (PR `#22`). Qualquer falha no `check_site.sh` bloqueia a integração na `main`. |

*Fonte: Elaborado pelos autores.*

---

## 5. Calendário de Medições do Projeto

As coletas formais de avaliação e decisão seguem os marcos da disciplina registrados na Tabela 5, além da atualização diária automatizada via GitHub Actions.

**Tabela 5 — Calendário de medições e pontos de decisão da gestão**

| Medição | Data de Corte | Marco de Referência | Escopo Analisado | Registro das Decisões |
| :---: | :---: | :--- | :--- | :--- |
| **Medição 1** | `27/10/2026` | Fechamento da Entrega 1 (`v1.0.0-pc1`) | Milestones `M0` a `M4` (Issues `#01` a `#19` e PRs `#20` a `#30`) | [Registro de Medições — Medição 1](registro-de-medicoes.md#medicao-1-fechamento-da-entrega-1-27102026) |
| **Retrospectiva E1** | `28/10/2026` | Pós-Entrega 1 | Análise crítica do processo da equipe e priorização das ações `C2` e `C4` | [Retrospectiva da Entrega 1](../sobre/retrospectiva-1.md) |
| **Medição 2** | `10/11/2026` | Planejamento da Entrega 2 e Abertura M5/M6 | Auditoria de transição: 31 issues (`#01`–`#19` e `#38`–`#49`) e 19 PRs integrados | [Registro de Medições — Medição 2](registro-de-medicoes.md#medicao-2-transicao-e-abertura-da-entrega-2-10112026) |
| **Medição 3** | *Final da E2* | Fechamento da Entrega 2 (`v2.0.0-pc2`) | Conclusão dos Milestones `M5` e `M6`, apuração final de `VEC` e `ACM` | A consolidar no fechamento do Ponto de Controle 2 |

*Fonte: Elaborado pelos autores.*
