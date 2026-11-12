# Registro de Medições e Decisões (PSM/CID)

No ciclo do **PSM (*Practical Software and Systems Measurement*)**, a coleta de dados só gera valor gerencial quando cada medição é seguida de **interpretação crítica**, **identificação de limitações do próprio processo de medição** e **decisão concreta de gestão**.

Esta página registra os pontos de medição formal da equipe **Grace Hopper**, seguindo os critérios estabelecidos no [Plano de Medição da Gestão](plano-de-medicao.md). Os gráficos atualizados diariamente podem ser consultados no [Painel de Indicadores PSM/CID](../indicadores_psm.md).

---

## Medição 1 — Fechamento da Entrega 1 (`27/10/2026`)

**Contexto e Linha de Base:** Coleta realizada no fechamento do Ponto de Controle 1 (Release `v1.0.0-pc1`), abrangendo os milestones `M0` a `M4` (19 issues planejadas: `#01` a `#19`) e os 11 pull requests integrados no período (`#20` a `#30`).

### 1.1 Quadro de Valores, Interpretação e Decisões (Medição 1)

**Tabela 1 — Avaliação dos indicadores PSM/CID no fechamento da Entrega 1**

| Categoria PSM | Indicador | Valor Medido em 27/10/2026 | Interpretação Técnica | Decisão de Gestão para a Etapa Seguinte |
| :--- | :---: | :--- | :--- | :--- |
| **Calendário e Progresso** | **`TCM`** | `M0`: 1/1 · `M1`: 6/6 · `M2`: 5/5 · `M3`: 3/3 · `M4`: 4/4<br>**Total: 19/19 (100,0%)** | Todas as 19 issues planejadas para as Fases 1, 2 e 3 foram concluídas até a publicação da Release E1. Contudo, houve concentração de fechamentos nos dias finais antes da entrega. | Estruturar a Entrega 2 desde o início em 12 issues atômicas (`#38` a `#49`) nos milestones `M5` e `M6`, já com responsável e estimativa definidos. |
| **Calendário e Progresso** | **`ACM`** | **Não calculável (`n/c`)** | Os milestones `M0` a `M4` foram criados no GitHub sem o preenchimento do campo *Due date* (`due_on`), impossibilitando o cálculo automático de atraso/adiantamento por marco. | Cadastrar datas-limite explícitas nos milestones `M5` e `M6` para viabilizar o cálculo de `ACM` e do desvio em dias na Entrega 2. |
| **Recursos e Custos** | **`VEC`** | **0,0%**<br>*(63h realizadas / 63h planejadas nas 17 issues apontadas na data; 55h/55h em 14 issues via parser da API)* | Embora o orçamento consolidado da equipe tenha fechado em `72h` (`R$ 3.600,00`), nas issues com registro as horas realizadas foram preenchidas com o mesmo valor das horas estimadas, e parte das issues ficou sem o campo numérico atualizado na API. | Exigir apontamento do tempo realmente gasto (com fração de hora se necessário) ao fechar cada issue da Entrega 2, distinguindo linha de base planejada de esforço efetivo. |
| **Desempenho dos Processos** | **`TRCD`** | **9/11 (81,8%)** global<br>**9/9 (100,0%)** pós-workflow | Os PRs `#20` e `#21` foram integrados antes da criação do workflow de build estrito (introduzido no PR `#22`). Após a ativação do CI, 100% dos PRs integrados passaram por `mkdocs build --strict` e `check_site.sh`. | Manter o build estrito e a revisão por par como requisito bloqueante para qualquer merge na branch `main`. |

*Fonte: Elaborado pelos autores a partir dos registros do repositório e da Seção III-C do artigo científico da Entrega 1.*

---

## Alinhamento com a Retrospectiva da Entrega 1 (`28/10/2026`)

No dia seguinte ao fechamento da Medição 1, a equipe conduziu a [Retrospectiva da Entrega 1](../sobre/retrospectiva-1.md), aplicando a dinâmica dos *Três Porquinhos* e o plano de ação *Quê-Quem-Quando*. A análise qualitativa da equipe confirmou os achados quantitativos do PSM:

- **Causa raiz identificada (*Casa de Palha*):** Início tardio das tarefas do primeiro ponto de controle, gerando acúmulo de entregas próximo ao prazo final.
- **Pontos fortes preservados (*Casa de Tijolos*):** Comunicação rápida, revisão cruzada constante (refletida na alta taxa de aprovação de PRs) e automação do repositório.
- **Ações corretivas priorizadas por unanimidade (6 votos cada):**
  1. **Tópico `C2` (Participação contínua):** Acompanhamento semanal da movimentação de issues e commits no GitHub, sob coordenação de **Fábio Santos Araujo**, usando o indicador `TCM` e o [Painel em Tempo Real](../painel_projeto.md).
  2. **Tópico `C4` (Revisão prévia dos critérios de avaliação):** Antes de cada ponto de controle, todos os integrantes devem validar seus entregáveis contra o checklist da rubrica da disciplina, sustentando o indicador `TRCD` em 100%.

---

## Medição 2 — Transição e Abertura da Entrega 2 (`10/11/2026`)

**Contexto:** Coleta automatizada após a consolidação das revisões pós-PC1 e abertura formal do backlog da Entrega 2 (Issues `#38` a `#49` distribuídas nos milestones `M5` e `M6`).

### 2.1 Quadro de Valores, Interpretação e Decisões (Medição 2)

**Tabela 2 — Avaliação dos indicadores PSM/CID na transição para a Entrega 2**

| Indicador | Valor Apurado pelo Painel | Interpretação do Estado Atual | Decisão e Próximo Passo |
| :--- | :---: | :--- | :--- |
| **`TCM`** | **19/31 (61,3%)** acumulado<br>*(E1: 19/19 = 100% · E2: 0/12 = 0%)* | A queda percentual de `100%` para `61,3%` decorre da abertura planejada das 12 novas issues da Entrega 2 (`M5`: 8 issues; `M6`: 4 issues). O escopo da E2 já está 100% cadastrado e atribuído no GitHub. | Iniciar a execução da **Trilha A (`#38`)** (subida do ambiente Docker do i-Educar 2.12), que é pré-requisito para as medições de `M1` a `M15`. |
| **`TRCD`** | **17/19 (89,5%)** global<br>**17/17 (100,0%)** pós-workflow | Entre o corte de 27/10 e 10/11, mais 8 PRs foram integrados para refinamento do artigo e da GitPage. Todos os 17 PRs posteriores ao PR `#22` passaram no build estrito (`100%`). | Preservar a validação automática em `.github/workflows/pages.yml` durante a reformulação visual da GitPage. |
| **Aprovação antes do merge** | **18/19 (94,7%)** dos PRs integrados | Apenas 1 PR inicial (`#22`, que configurou o próprio workflow) foi integrado sem aprovação formal registrada; todos os demais 18 PRs tiveram revisão aprovada por outro integrante. | Manter a revisão cruzada obrigatória em todas as entregas das Trilhas A a F. |
| **`VEC`** | **0,0%**<br>*(55,0h reais / 55,0h estimadas em 14 issues lidas pela API)* | O coletor identificou 5 issues concluídas da E1 (`#09`, `#10`, `#11`, `#12`, `#14`) onde o campo `Esforço Efetivo Realizado` no corpo da issue do GitHub ainda não continha valor numérico parseável. | Atualizar os comentários/corpo das issues ao fechá-las para que 100% das issues concluídas entrem no denominador automático do `VEC`. |

*Fonte: Dados coletados automaticamente por `scripts/psm/coletar_dados.py` em 10/11/2026.*

---

## Medição 3 — Execução da Entrega 2 e Auditoria de Contribuição (`12/11/2026`)

**Contexto:** Coleta realizada durante a execução das Trilhas técnicas da Entrega 2, acompanhada da modernização visual da GitPage (reativação do índice lateral direito) e da inclusão de gráficos analíticos de tempo de ciclo, horas estimadas vs. reais e matriz de contribuição por integrante.

### 3.1 Quadro de Valores, Interpretação e Decisões (Medição 3)

**Tabela 3 — Avaliação dos indicadores PSM/CID na Medição 3**

| Indicador | Valor Apurado pelo Painel | Interpretação do Estado Atual | Decisão e Próximo Passo |
| :--- | :---: | :--- | :--- |
| **`TCM`** | **19/31 (61,3%)** acumulado<br>*(E1: 19/19 = 100% · E2: 0/12 = 0%)* | As 19 issues da Entrega 1 permanecem concluídas. As 12 issues da Entrega 2 estão em execução ativa pelas Trilhas A a F, com previsão de entrega nos marcos M5 e M6. | Manter a cadência de desenvolvimento nas trilhas técnicas do i-Educar e monitorar pull requests em andamento. |
| **`TRCD`** | **21/23 (91,3%)** global<br>**21/21 (100,0%)** pós-workflow | Todos os 21 PRs integrados desde a implantação do workflow de validação passaram com sucesso em `mkdocs build --strict` e `check_site.sh`. | Manter a execução mandatória do build estrito em todos os novos PRs. |
| **Aprovação antes do merge** | **22/23 (95,7%)** dos PRs integrados | Excelente adesão ao `CONTRIBUTING.md`, com apenas 1 PR não auditado previamente antes da ativação do CI. | Preservar a revisão por pares obrigatória. |
| **`VEC`** | **-34,3%**<br>*(71,0h reais vs. 108,0h estimadas nas issues apontadas)* | A variação reflete que parte das issues concluídas apontou esforço efetivo menor que o limite máximo estimado, e 5 issues concluídas ainda demandam formalização de horas. | Realizar auditoria fina de apontamentos nas issues de fechamento da Entrega 2. |
| **Tempo de Ciclo Médio (`TC`)** | **7,7 dias** (mín: 1,5d; máx: 12,0d) | O tempo médio de resolução das tarefas encontra-se perfeitamente contido na faixa operacional sem investigação estipulada pelo PSM (3,0 a 10,0 dias). | Continuar o monitoramento visual através do gráfico de dispersão de tempo de ciclo no painel PSM. |

*Fonte: Dados coletados automaticamente por `scripts/psm/coletar_dados.py` em 12/11/2026.*

---

## Avaliação do Próprio Processo de Medição e Melhorias Implementadas

Seguindo a recomendação do guia PSM/CID de auditar também a eficácia do sistema de medição, a equipe identificou e corrigiu nesta revisão da GitPage três limitações que dificultavam o acompanhamento:

1. **Inclusão do `VEC` no Painel Automático:** Anteriormente, `scripts/psm/indicadores.py` calculava a função `vec(dados)`, mas `scripts/docs/gen_indicadores.py` exibia apenas 3 cartões (`TCM`, `TRCD`, `ACM`). O gerador foi atualizado para exibir o **4º cartão (`VEC`)** e a seção dedicada de **Recursos e Custos** com auditoria das issues sem apontamento.
2. **Despoluição Visual e Estrutura em 3 Etapas:** A documentação de gestão estava concentrada em um único arquivo de mais de 800 linhas. A divisão em **Planejar**, **Medir** e **Avaliar e Decidir** permite localizar qualquer indicador, fórmula ou decisão em segundos.
3. **Fichas de Medição Padronizadas:** Cada seção do painel automático passou a exibir uma ficha-resumo com *O que mede*, *Fórmula*, *Fonte dos dados* e *Critério de decisão*, conectando a visualização gráfica diretamente à tomada de decisão.
