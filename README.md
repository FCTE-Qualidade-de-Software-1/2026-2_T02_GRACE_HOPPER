# Avaliação de Qualidade de Software — i-Educar (`projeto-qualidade`)

[![Norma ISO/IEC 25010:2023](https://img.shields.io/badge/Norma-ISO%2FIEC%2025010%3A2023-blue.svg)](https://www.iso.org/standard/78176.html)
[![Norma ISO/IEC 25040:2024](https://img.shields.io/badge/Processo-ISO%2FIEC%2025040%3A2024-green.svg)](https://www.iso.org/standard/83642.html)
[![Metodologia GQM](https://img.shields.io/badge/Metodologia-GQM%20v2.0-orange.svg)](docs/gqm_evaluation_framework.md)
[![Status da Release](<https://img.shields.io/badge/Release-E2%20(v2.0.0--pc2)-purple.svg>)](docs/gestao_projeto_releases_milestones_issues.md)
[![Documentação GitHub Pages](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/)

<section class="gh-hero">
  <p class="gh-hero__eyebrow">Universidade de Brasília · FGA · Qualidade de Software 1</p>
  <p class="gh-hero__lead">Uma avaliação sistemática da qualidade do <strong>i-Educar</strong>, conectando normas internacionais, métricas e evidências técnicas.</p>
  <div class="gh-hero__meta">
    <span>Projeto acadêmico</span>
    <span>Semestre 2026.2</span>
    <span>Release E2 · v2.0.0-pc2</span>
  </div>
  <div class="gh-hero__actions">
    <a class="gh-button gh-button--primary" href="https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/gqm_evaluation_framework/">Explorar framework GQM</a>
    <a class="gh-button gh-button--secondary" href="https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/plano_medicao_testes/">Ver resultados Fases 4 e 5</a>
  </div>
</section>

O projeto avalia o sistema livre de gestão escolar **i-Educar** no âmbito da disciplina **Qualidade de Software 1 (FGA0315)** da **Universidade de Brasília (UnB / FGA)**.

---

## 1. Identificação da Equipe e Gestão de Recursos (PSM/CID — Critério AG-C5)

As Tabelas 1 e 1-B registram os membros da equipe avaliadora, com identificação individual, papel, valor/hora de trabalho e esforço planejado e realizado no **Ponto de Controle 1 (Entrega 1)** e no **Ponto de Controle 2 (Entrega 2)**.

**Tabela 1 — Identificação da equipe avaliadora, papéis e alocação de esforço no Ponto de Controle 1 (Entrega 1)**

| Integrante                                | Matrícula UnB |  Usuário GitHub   | Papel Principal (Entrega 1 — Fases 1 a 3)                               | Horas (h) |   Valor / Hora    |   Custo Total   | % Esforço  |
| :---------------------------------------- | :-----------: | :---------------: | :---------------------------------------------------------------------- | :-------: | :---------------: | :-------------: | :--------: |
| **Arthur Soares Parente**                 | `23/2036770`  | `@ArthurDevWorks` | Gestor de Configuração / GitPage (Issues #01, #09–#12, #15, #16, #18)   |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Fábio Santos Araujo**                   | `22/2022082`  | `@fabiofonteles1` | Redação do Artigo (Overleaf) e Slides PC1 (Issues #13, #14, #18)        |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Gabriel Barbaceli**                     | `21/1045122`  |   `@Nibaacriba`   | GitPage / Especificação GQM de G1 e G4 (Issues #05, #08, #17, #19)      |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Gustavo Silva Rodrigues**               | `23/2036887`  |  `@g-srodrigues`  | Analista de Qualidade / Modelo ISO/IEC 25010 e Escopo (Issues #04, #13) |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira**       | `23/2037937`  |   `@ItaloSamP`    | Analista do Produto, Stakeholders e GQM G2/G3 (Issues #02, #03, #06, #07) |  12h    |     R$ 50,00      |    R$ 600,00    | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409`  |   `@ChickRicks`   | Revisão da GitPage e do artigo                                          |    12h    |     R$ 50,00      |    R$ 600,00    | **16,66%** |
| **TOTAL CONSOLIDADO (E1)**                |       —       |         —         | **Esforço Acumulado — Ponto de Controle 1 (`19/19` issues)**            |  **72h**  | Média: R$ 50,00/h | **R$ 3.600,00** |  **100%**  |

*Fonte: Elaborado pelos autores conforme diretrizes da disciplina FGA0315 e modelo PSM/CID.*

**Tabela 1-B — Alocação de papéis, esforço planejado e realizado no Ponto de Controle 2 (Entrega 2 — `v2.0.0-pc2`)**

| Integrante                                | Matrícula UnB |  Usuário GitHub   | Papel Principal e Entregas na Entrega 2 (Fases 4 e 5)                                  | Issues GitHub | Horas Plan. (Reais) | Valor / Hora | Custo Plan. (Real) | % Esforço Plan. |
| :---------------------------------------- | :-----------: | :---------------: | :------------------------------------------------------------------------------------- | :-----------: | :-----------------: | :----------: | :----------------: | :-------------: |
| **Arthur Soares Parente**                 | `23/2036770`  | `@ArthurDevWorks` | Arquitetura (`M8`, `M9`, `M11`), Proteção (`Gate M12`) e Mensagens (`M13` — PR #55)    | `#44`, `#45`  |   12h (`12,0h`)     |   R$ 50,00   | R$ 600 (`R$ 600`)  |   **16,67%**    |
| **Fábio Santos Araujo**                   | `22/2022082`  | `@fabiofonteles1` | Agregação `IQC`/`IQM`, Parecer Fase 5, Slides PC2, Auditoria PSM/CID e Release E2      | `#47`, `#49`  |   12h (`12,0h`)     |   R$ 50,00   | R$ 600 (`R$ 600`)  |   **16,67%**    |
| **Gabriel Barbaceli**                     | `21/1045122`  |   `@Nibaacriba`   | Motor Estático AST (`M7a/b`, `M10`), Renormalização `M14/M15` e Melhoria (`#56`)       | `#43`, `#46`, `#56` | 12h (`12,0h`) |   R$ 50,00   | R$ 600 (`R$ 600`)  |   **16,67%**    |
| **Gustavo Silva Rodrigues**               | `23/2036887`  |  `@g-srodrigues`  | Oráculo Pedagógico Determinístico (`Gate M3 — DCNM = 100%`) e Artigo Científico v2     | `#40`, `#48`  |   12h (`6,0h`)      |   R$ 50,00   | R$ 600 (`R$ 300`)  |   **16,67%**    |
| **Ítalo Alves Sampaio de Oliveira**       | `23/2037937`  |   `@ItaloSamP`    | Ambiente Docker, Coexistência (`M1 = 100%`) e Contratos REST (`M2 = 90%` — PR #52)     | `#38`, `#39`  |   12h (`12,0h`)     |   R$ 50,00   | R$ 600 (`R$ 600`)  |   **16,66%**    |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409`  |   `@ChickRicks`   | Trilha de Atomicidade Transacional (`Gate M4 — ITAE`), `M5` e Backup (`M6 — CVPB`)     | `#41`, `#42`  |   12h (`0,0h`)      |   R$ 50,00   | R$ 600 (`R$ 0`)    |   **16,66%**    |
| **TOTAL CONSOLIDADO (E2)**                |       —       |         —         | **Esforço Consolidado — Ponto de Controle 2 (`10/13` issues concluídas/PR)**           | `#38`–`#49`, `#56` | **72h (`54,0h`)** | **R$ 50,00/h** | **R$ 3.600 (`R$ 2.700`)** | **100%** |

*Fonte: Elaborado pelos autores com base na auditoria automatizada de `scripts/psm/coletar_dados.py` em 15/11/2026.*

_Nota: O esforço planejado em cada etapa foi dividido igualmente entre os 6 integrantes ($4 \times 16{,}67\% + 2 \times 16{,}66\% = 100\%$, totalizando `144h` e `R$ 7.200,00` planejados no projeto completo E1 + E2, com `126,0h` nominais / `124,0h` apontadas nas issues concluídas)._

---

## 2. Objeto de Avaliação e Escopo Tecnológico

O software avaliado é o **i-Educar** (versão 2.12.0 / repositório base `portabilis/i-educar`), um monólito híbrido que articula um núcleo legado em PHP (`ieducar/`) a uma infraestrutura moderna em Laravel 13 com banco de dados relacional PostgreSQL.

A avaliação concentra-se em dois módulos funcionais de alta criticidade, cujos componentes e escopo estão discriminados na Tabela 2:

**Tabela 2 — Módulos funcionais prioritários do i-Educar sob avaliação**

| Módulo Avaliado                      | Tabelas Principais (PostgreSQL)                                                                                                    | Classes e Controladores-Chave                                                                                                      | Escopo Funcional                                                                                                                          |
| :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Matrícula de Alunos**           | `pmieducar.matricula`<br>`pmieducar.matricula_turma`                                                                               | `LegacyRegistration`<br>`LegacyEnrollment`<br>`RegistrationStatus`<br>`RegistrationService`                                        | Vínculo formal do estudante, enturmação, remanejamento, ciclo de vida de 14 situações escolares e cancelamento atômico transacional.      |
| **2. Lançamento de Notas e Menções** | `modules.regra_avaliacao`<br>`modules.tabela_arredondamento_valor`<br>`modules.nota_aluno`<br>`modules.nota_componente_curricular` | `LegacyEvaluationRule`<br>`LegacyValueRoundingTable`<br>`DiarioController`<br>`DiarioApiController`<br>`Avaliacao_Service_Boletim` | Regras pedagógicas configuráveis, tabelas dinâmicas de menção/arredondamento, controle do diário eletrônico e motor de cálculo de médias. |

*Fonte: Elaborado pelos autores a partir do repositório oficial portabilis/i-educar.*

---

## 3. Fundamentação Normativa e Metodológica

A avaliação é conduzida seguindo estritamente as normas internacionais vigentes e frameworks de engenharia, sintetizados na Tabela 3:

**Tabela 3 — Normas internacionais e metodologias adotadas na avaliação**

| Norma / Framework                                     | Papel na Avaliação             | Recorte Aplicado ao i-Educar                                                                                                                                                                                                                                                                                                                              |
| :---------------------------------------------------- | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ISO/IEC 25010:2023** (_Product Quality Model_)      | Modelo de Qualidade de Produto | **Compatibilidade** (Coexistência e Interoperabilidade), **Confiabilidade** (Ausência de Falhas / _Faultlessness_, Tolerância a Falhas e Recuperabilidade), **Manutenibilidade** (Modularidade, Analisabilidade, Modificabilidade e Testabilidade) e **Capacidade de Interação** (_Interaction Capability_ — Proteção contra Erros e Autodescritividade). |
| **ISO/IEC 25019:2023** (_Quality-in-Use Model_)       | Modelo de Qualidade em Uso     | Avaliação da **Eficácia** e **Eficiência** em contexto de uso escolar real (tempo de tarefa e sucesso de primeira tentativa no diário e na matrícula).                                                                                                                                                                                                    |
| **ISO/IEC 25040:2024** (_Quality Evaluation Process_) | Processo de Avaliação          | Ciclo estruturado em 5 atividades (Requisitos, Especificação, Desenho, Execução e Julgamento).                                                                                                                                                                                                                                                            |
| **Metodologia GQM** (_Goal-Question-Metric_)          | Derivação de Métricas          | Desdobramento formal em 4 objetivos, 14 questões, 15 famílias e 17 linhas operacionais (M7a/b e M14a/b desdobradas), com 3 Gates Binários eliminatórios.                                                                                                                                                                                                  |
| **Framework PSM/CID**                                 | Gestão de Recursos e Custos    | Rastreamento de métricas de processo, custos financeiros e esforço dedicado da equipe.                                                                                                                                                                                                                                                                    |

*Fonte: Elaborado pelos autores com base nas normas ISO/IEC e referências metodológicas da disciplina.*

---

## 4. Execução, Julgamento Multicritério e Decisão (Fases 4 e 5 — ISO/IEC 25040:2024)

A avaliação empírica sobre o commit congelado `7903a3efc7689942ee700007f86ed581023aad27` do **i-Educar 2.12** produziu os seguintes resultados consolidados (detalhados nas [Seções 8 e 9 do Plano Operacional de Medição e Testes](docs/plano_medicao_testes.md)):

- **Gates Binários Eliminatórios (Etapa 1):**
  - **Gate 1 (`M3 — DCNM`):** **APROVADO (`100,0%`**, `30/30` cenários do oráculo pedagógico e `457` asserções executadas sobre `Boletim.php`).
  - **Gate 2 (`M4 — ITAE`):** **NÃO COMPROVADO / BLOQUEADO** (sem coleta concluída na Issue `#41`; pela regra não-compensatória da Seção 5.1, evidência ausente mantém o gate bloqueado).
  - **Gate 3 (`M12 — IPPE`):** **APROVADO (`100,0%`**, `12/12` cenários de entradas inválidas bloqueados sem erro HTTP 500 e com variação nula no PostgreSQL, $\Delta\text{DB} = 0$).
- **Índices por Característica ($\text{IQC}_k$) e Ação de Melhoria (Issue `#56`):**
  - **$\text{IQC}_{\text{Comp}}$ (Peso $20\%$):** **$3{,}50$** (`M1: TINCR = 100,0%`, $S=4$; `M2: CEI = 90,0%`, $S=3$).
  - **$\text{IQC}_{\text{Conf}}$ (Peso $30\%$):** **$4{,}00$ parcial em `M3`** (suspenso até a comprovação de `M4` e `M6`; `M5` excluída pela Seção 3.1).
  - **$\text{IQC}_{\text{Manut}}$ (Peso $30\%$):** **$2{,}20$ no commit congelado** (`M7a = 8`, $S=4$; `M7b = 72`, $S=1$; `M8 = 0,3784`, $S=2$; `M9 = 4,5556`, $S=1$; `M10 = 63,82`, $S=3$; `M11 = 78,92%`, $S=2$). Com a aplicação do patch da **Issue `#56` (`getSituacaoNotas.patch`, provado equivalente em 50.000 cenários com 0 divergências)**, a complexidade de `getSituacaoNotas` cai de $72$ para $15$, reduzindo `M7b` para $30$ ($S: 1 \to 3$) e elevando **$\text{IQC}_{\text{Manut}}$ para $2{,}60 \ge 2{,}50$**.
  - **$\text{IQC}_{\text{Interação}}$ (Peso $20\%$):** **$3{,}14$** (`M12 = 100,0%`, $S=4$; `M13 = 75,00%`, $S=1$; `M14a/b` e `M15` excluídas antes da coleta pela Seção 3.4).
- **Índice Global ($\text{IQM}$) e Classificação Final da Release:**
  - **No commit congelado (`7903a3e`):** $\text{IQM}_{\text{base}} = \mathbf{3{,}19}$ (ou $\mathbf{2{,}84}$ sobre G1+G3+G4) $\implies$ **CLASSE C (Reprovado / Bloqueado)** devido a $\text{IQC}_{\text{Manut}} = 2{,}20 < 2{,}50$ e ao Gate M4 pendente.
  - **Pós-Ação de Melhoria (`#56`):** $\text{IQM}_{\text{pós-melhoria}} = \mathbf{3{,}31}$ (ou $\mathbf{3{,}01}$ sobre G1+G3+G4) $\implies$ **Transição técnica para a CLASSE B (Aprovado com Ressalvas)** mediante homologação do Gate M4.

---

## 5. Estrutura e Mapa de Documentação do Projeto

A documentação do projeto está organizada em módulos temáticos, detalhados na Tabela 4 com os respectivos caminhos de acesso e escopos de conteúdo:

**Tabela 4 — Mapa de artefatos e navegação da documentação técnica**

| Artefato Documental                         | Caminho no Repositório                                                                                                             | Conteúdo Principal                                                                                                                                                    |
| :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Apresentação Final — PC2 (Entrega 2)**    | [`docs/apresentacao_pc2.pdf`](docs/apresentacao_pc2.pdf) · [`docs/apresentacao_pc2.pptx`](docs/apresentacao_pc2.pptx)              | Slides finais da Entrega 2 (11 lâminas): resultados de M1 a M15, Ação de Melhoria (`#56`), cálculo de $\text{IQC}_k$/$\text{IQM}$, parecer por stakeholder e PSM/CID. |
| **Plano Operacional e Julgamento Fase 5**   | [`docs/plano_medicao_testes.md`](docs/plano_medicao_testes.md)                                                                     | Roteiro operacional (M1 a M15), resultados da Fase 4 (Seções 6 a 8) e conclusão da Fase 5 (Seção 9: Gates, $\text{IQC}_k$, $\text{IQM}$, backlog e parecer técnico). |
| **Framework GQM de Avaliação (v2.0)**       | [`docs/gqm_evaluation_framework.md`](docs/gqm_evaluation_framework.md)                                                             | Objeto de avaliação, árvores GQM por característica, fórmulas matemáticas (M1 a M15), limiares, regras de decisão e quadro consolidado da Fase 5 (Seção 7).          |
| **Relatório da Medição M3 (Gate DCNM)**     | [`docs/fase-4/medicao_m3_dcnm.md`](docs/fase-4/medicao_m3_dcnm.md)                                                                 | Execução oficial dos 30 cenários do oráculo de notas e menções (`oficial-001`, 457 asserções, $\text{DCNM} = 100\%$).                                                |
| **Relatório de Manutenibilidade (M7 e M10)**| [`docs/fase-4/manutenibilidade-m7-m10.md`](docs/fase-4/manutenibilidade-m7-m10.md)                                                 | Extração estática AST dos 213 callables no commit `7903a3e` ($\text{CC}_{P90} = 8$, $\text{CC}_{\max} = 72$, $\text{MI} = 63{,}82$).                                  |
| **Planejamento do Ponto de Controle 1**     | [`docs/relatorio_de_planejamento_ponto_de_controle_1_i_educar.md`](docs/relatorio_de_planejamento_ponto_de_controle_1_i_educar.md) | Linha do tempo (M0 a M5), requisitos da Fase 1, matriz de priorização ($C = I \times R$), resumo GQM e apresentação PC1 ([`PDF`](docs/apresentacao_pc1.pdf)).        |
| **Visão do Produto e Arquitetura**          | [`docs/agents/project_overview.md`](docs/agents/project_overview.md) · [`docs/agents/architecture.md`](docs/agents/architecture.md)| Descrição do sistema avaliado, arquitetura híbrida Laravel 13 + legado PHP, versões verificadas e esquemas PostgreSQL.                                               |
| **Gestão de Milestones, Issues e Releases** | [`docs/gestao_projeto_releases_milestones_issues.md`](docs/gestao_projeto_releases_milestones_issues.md)                           | Alocação de custos PSM/CID (E1 e E2), diagrama de marcos M0 a M6, catálogo atômico das Issues `#01` a `#56` e especificação das Releases E1 e E2 (`v2.0.0-pc2`).     |
| **Guia de Contribuição e Governança Git**   | [`CONTRIBUTING.md`](CONTRIBUTING.md)                                                                                               | Fluxo de trabalho de issues, branches, padrão de commits e política de revisão por pares.                                                                             |

*Fonte: Elaborado pelos autores.*

---

## 6. Execução Local da Documentação (GitHub Pages)

A documentação do projeto é construída com o gerador estático [MkDocs](https://www.mkdocs.org/) e o tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). Para executar o ambiente localmente e visualizar o site:

### 6.1 Pré-requisitos

- Python 3.10 ou superior
- Gerenciador de pacotes `pip`

### 6.2 Passo a Passo para Execução Local

1. **Criar e ativar o ambiente virtual**:

   ```bash
   python3 -m venv .venv-docs
   source .venv-docs/bin/activate
   ```

2. **Instalar as dependências de documentação**:

   ```bash
   pip install -r requirements-docs.txt
   ```

3. **Iniciar o servidor de desenvolvimento**:

   ```bash
   mkdocs serve
   ```

   O site estará acessível no navegador em `http://127.0.0.1:8000/`.

4. **Validar o build estrito e integridade dos links**:
   ```bash
   bash scripts/docs/check_site.sh
   ```
   _(O script executa `mkdocs build --strict` e valida títulos, links e fórmulas renderizadas)._

---

## 7. Governança e Declaração de Uso de Ferramentas de IA (Critério AG-C3)

Durante a preparação das Entregas 1 e 2, ferramentas de inteligência artificial apoiaram a organização da documentação, o desenvolvimento da GitPage, a codificação de scripts coletores, a geração das apresentações de slides (PC1 e PC2) e a elaboração do artigo. As declarações abaixo relacionam o uso informado por cada integrante à sua participação no trabalho. A descrição das tarefas e a descrição do apoio de IA são apresentadas separadamente para registrar o papel de cada ferramenta (consulte também a [Declaração completa na GitPage](docs/sobre/uso-de-ia.md)).

### 7.1 Ítalo Alves Sampaio de Oliveira

- **Participação no trabalho:** Na Entrega 1, contextualização do i-Educar, arquitetura, stakeholders, ODS 4/16 e especificação GQM de Confiabilidade e Manutenibilidade (`#02`, `#03`, `#06`, `#07`). Na Entrega 2, provisionamento do ambiente Docker do i-Educar 2.12, ensaio de coexistência de instâncias (`M1 — TINCR = 100%`) e testes de contrato JSON Schema dos 10 endpoints REST (`M2 — CEI = 90%`) (`#38`, `#39`, PR `#52`).
- **Ferramentas utilizadas:** OpenCode e Claude.
- **Apoio de IA declarado:** Auxílio ao desenvolvimento da GitPage, elaboração dos scripts `m1_coexistencia.sh` e `m2_cei.py` e estruturação dos JSON Schemas a partir dos controllers. Todas as execuções em container e classificações de conformidade foram validadas pelo autor.

### 7.2 Gabriel Barbaceli

- **Participação no trabalho:** Na Entrega 1, propósito e uso pretendido da avaliação, matriz de priorização, especificação GQM de Compatibilidade e de Capacidade de Interação/Qualidade em Uso e quadro de integrantes (`#05`, `#08`, `#17`, `#19`). Na Entrega 2, evolução e execução do motor estático AST (`M7a`, `M7b`, `M10`), formalização da regra pré-coleta de `M14a/b` e `M15` e execução da Ação de Melhoria sobre `getSituacaoNotas` com 50.000 testes de equivalência (`#43`, `#46`, `#56`, PRs `#53` e `#57`).
- **Ferramenta utilizada:** Claude.
- **Apoio de IA declarado:** Apoio na codificação do parser AST em PHP e do arnês de teste diferencial de equivalência, bem como refinamento textual dos relatórios da GitPage. Os cálculos e o patch de refatoração foram integralmente verificados por execução real.

### 7.3 Fábio Santos Araujo

- **Participação no trabalho:** Na Entrega 1, elaboração do artigo, preparação dos slides PC1 e melhorias na GitPage (`#13`, `#14`, `#18`). Na Entrega 2, agregação multicritério da Fase 5 ($\text{IQC}_k$ e $\text{IQM}$), julgamento dos Gates Binários, parecer técnico por stakeholder, elaboração dos slides finais do PC2 (`docs/apresentacao_pc2.pptx` e `docs/apresentacao_pc2.pdf`), auditoria de horas e custos PSM/CID (`Medição 3`) e publicação da Release E2 (`v2.0.0-pc2`) (`#47`, `#49`).
- **Ferramentas utilizadas:** GitHub Copilot e Gemini (Antigravity).
- **Apoio de IA declarado:** Auxílio na conferência algébrica das memórias de cálculo da Fase 5, geração programática dos slides PC2 e reconciliação automatizada de metadados das issues no GitHub. Todos os números, equações e pareceres foram conferidos contra as evidências brutas da Fase 4.

### 7.4 Arthur Soares Parente

- **Participação no trabalho:** Na Entrega 1, infraestrutura do repositório, automação da GitPage, limiares, planejamento Docker/AST/TCLE e Release E1 (`#01`, `#09`–`#12`, `#15`, `#16`, `#18`). Na Entrega 2, medição de acoplamento (`M8 — DSPM`), fricção legado-moderno (`M9 — IFDL`), testes ativos com asserção (`M11 — TTAE`), proteção contra erros (`Gate M12 — IPPE = 100%`) e autodescritividade de mensagens (`M13 — ADMV = 75%`) (`#44`, `#45`, PR `#55`).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA declarado:** Apoio à automação dos scripts de extração estática e de submissão dos 12 cenários inválidos contra o container oficial do i-Educar, além da revisão documental frente às rubricas. Todas as saídas HTTP, consultas SQL e contagens de testes foram auditadas manualmente.

### 7.5 Gustavo Silva Rodrigues

- **Participação no trabalho:** Na Entrega 1, adaptação do modelo de qualidade ISO/IEC 25010:2023, delimitação do escopo e coautoria do artigo (`#04`, `#13`). Na Entrega 2, construção do manifesto congelado de 30 casos do oráculo pedagógico e execução da suíte determinística do `Gate M3 (DCNM = 100%)` sobre `Boletim.php`, além da consolidação do Artigo v2 (`#40`, `#48`, PR `#54`).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA declarado:** Auxílio à estruturação do runner de testes PHPUnit do oráculo (`M3OracleTest.php`), consolidação dos logs JSON/JUnit e escrita em LaTeX. Todas as regras pedagógicas e asserções foram confrontadas com o código-fonte do i-Educar.

### 7.6 Ricardo Lucas Winchello Vieira Branco

- **Participação no trabalho:** Revisão técnica cruzada da GitPage e validação de conformidade do artigo frente às rubricas na Entrega 1, e atribuição na trilha de confiabilidade complementar (`#41`, `#42`) na Entrega 2.
- **Supervisão e revisão humana:** Conferência independente de links, numeração de tabelas/figuras, somas percentuais de esforço e aderência entre os números reportados na GitPage e nas apresentações.

### 7.7 Revisão humana e responsabilidade pelo conteúdo

As sugestões foram revisadas e adaptadas pela equipe ao contexto do trabalho. Os integrantes mantêm a responsabilidade pelas decisões metodológicas, pela conferência das informações e pelo conteúdo apresentado no artigo e na GitPage. O uso de IA não substitui a consulta às fontes nem a verificação das definições, fórmulas e critérios utilizados.

### Medição M3 — Notas e menções (Entrega 2)

A coleta oficial da [issue #40](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/40) obteve **DCNM = 30/30 × 100% = 100%**, 457 asserções e **gate M3 APROVADO**. Consulte o [relatório](docs/fase-4/medicao_m3_dcnm.md) e as [evidências oficiais](evidencias/g2_confiabilidade/m3/oficial-001/summary.json). Os dez casos legados complementares registraram erro de pré-requisito de enturmação, relatado separadamente.

Com o Docker local preparado, a repetição diagnóstica é iniciada por `python3 scripts/avaliacao/m3/run_local.py`. O [guia do instrumento](scripts/avaliacao/m3/README.md) descreve a preparação e a execução oficial.
