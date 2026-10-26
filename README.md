# Avaliação de Qualidade de Software — i-Educar (`projeto-qualidade`)

[![Norma ISO/IEC 25010:2023](https://img.shields.io/badge/Norma-ISO%2FIEC%2025010%3A2023-blue.svg)](https://www.iso.org/standard/78176.html)
[![Norma ISO/IEC 25040:2024](https://img.shields.io/badge/Processo-ISO%2FIEC%2025040%3A2024-green.svg)](https://www.iso.org/standard/83642.html)
[![Metodologia GQM](https://img.shields.io/badge/Metodologia-GQM%20v2.0-orange.svg)](docs/gqm_evaluation_framework.md)
[![Status da Release](<https://img.shields.io/badge/Release-E1%20(v1.0.0--pc1)-purple.svg>)](docs/gestao_projeto_releases_milestones_issues.md)
[![Documentação GitHub Pages](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/)

<section class="gh-hero">
  <p class="gh-hero__eyebrow">Universidade de Brasília · FGA · Qualidade de Software 1</p>
  <p class="gh-hero__lead">Uma avaliação sistemática da qualidade do <strong>i-Educar</strong>, conectando normas internacionais, métricas e evidências técnicas.</p>
  <div class="gh-hero__meta">
    <span>Projeto acadêmico</span>
    <span>Semestre 2026.2</span>
    <span>Release E1 · v1.0.0-pc1</span>
  </div>
  <div class="gh-hero__actions">
    <a class="gh-button gh-button--primary" href="https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/gqm_evaluation_framework/">Explorar framework GQM</a>
    <a class="gh-button gh-button--secondary" href="https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/relatorio_de_planejamento_ponto_de_controle_1_i_educar/">Ver planejamento</a>
  </div>
</section>

O projeto avalia o sistema livre de gestão escolar **i-Educar** no âmbito da disciplina **Qualidade de Software 1 (FGA0315)** da **Universidade de Brasília (UnB / FGA)**.

---

## 1. Identificação da Equipe e Gestão de Recursos (PSM/CID — Critério AG-C5)

A tabela abaixo registra os membros da equipe avaliadora, com campos reservados para identificação individual, papel, valor/hora de trabalho e esforço planejado para o **Ponto de Controle 1 (Entrega 1)**.

| Integrante                                | Matrícula UnB |  Usuário GitHub   | Papel Principal                                                         | Horas (h) |   Valor / Hora    |   Custo Total   | % Esforço  |
| :---------------------------------------- | :-----------: | :---------------: | :---------------------------------------------------------------------- | :-------: | :---------------: | :-------------: | :--------: |
| **Arthur Soares Parente**                 | `23/2036770`  | `@ArthurDevWorks` | Gestor de Configuração / GitPage                                        |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Fábio Santos Araujo**                   | `22/2022082`  | `@fabiofonteles1` | Redação do Artigo (Overleaf)                                            |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Gabriel Barbaceli**                     | `21/1045122`  |   `@Nibaacriba`   | GitPage / Especificação GQM (Compatibilidade e Capacidade de Interação) |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Gustavo Silva Rodrigues**               | `23/2036887`  |  `@g-srodrigues`  | Analista de Qualidade / Modelo ISO/IEC 25010 e Escopo                   |    12h    |     R$ 50,00      |    R$ 600,00    | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira**       | `23/2037937`  |   `@ItaloSamP`    | Analista do Produto e Stakeholders / GitPage                            |    12h    |     R$ 50,00      |    R$ 600,00    | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409`  |   `@ChickRicks`   | Revisão da GitPage e do artigo                                          |    12h    |     R$ 50,00      |    R$ 600,00    | **16,66%** |
| **TOTAL CONSOLIDADO**                     |       —       |         —         | **Esforço Acumulado — Ponto de Controle 1**                             |  **72h**  | Média: R$ 50,00/h | **R$ 3.600,00** |  **100%**  |

_Nota: O esforço foi dividido igualmente entre os 6 integrantes (1/6 cada); os centésimos foram ajustados para que a soma seja exatamente 100%. Horas e custos devem ser atualizados conforme o andamento das issues associadas._

---

## 2. Objeto de Avaliação e Escopo Tecnológico

O software avaliado é o **i-Educar** (versão 2.12.0 / repositório base `portabilis/i-educar`), um monólito híbrido que articula um núcleo legado em PHP (`ieducar/`) a uma infraestrutura moderna em Laravel 13 com banco de dados relacional PostgreSQL.

A avaliação concentra-se em dois módulos funcionais de alta criticidade:

| Módulo Avaliado                      | Tabelas Principais (PostgreSQL)                                                                                                    | Classes e Controladores-Chave                                                                                                      | Escopo Funcional                                                                                                                          |
| :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Matrícula de Alunos**           | `pmieducar.matricula`<br>`pmieducar.matricula_turma`                                                                               | `LegacyRegistration`<br>`LegacyEnrollment`<br>`RegistrationStatus`<br>`RegistrationService`                                        | Vínculo formal do estudante, enturmação, remanejamento, ciclo de vida de 14 situações escolares e cancelamento atômico transacional.      |
| **2. Lançamento de Notas e Menções** | `modules.regra_avaliacao`<br>`modules.tabela_arredondamento_valor`<br>`modules.nota_aluno`<br>`modules.nota_componente_curricular` | `LegacyEvaluationRule`<br>`LegacyValueRoundingTable`<br>`DiarioController`<br>`DiarioApiController`<br>`Avaliacao_Service_Boletim` | Regras pedagógicas configuráveis, tabelas dinâmicas de menção/arredondamento, controle do diário eletrônico e motor de cálculo de médias. |

---

## 3. Fundamentação Normativa e Metodológica

A avaliação é conduzida seguindo estritamente as normas internacionais vigentes e frameworks de engenharia:

| Norma / Framework                                     | Papel na Avaliação             | Recorte Aplicado ao i-Educar                                                                                                                                                                                                                                                                                                                              |
| :---------------------------------------------------- | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ISO/IEC 25010:2023** (_Product Quality Model_)      | Modelo de Qualidade de Produto | **Compatibilidade** (Coexistência e Interoperabilidade), **Confiabilidade** (Ausência de Falhas / _Faultlessness_, Tolerância a Falhas e Recuperabilidade), **Manutenibilidade** (Modularidade, Analisabilidade, Modificabilidade e Testabilidade) e **Capacidade de Interação** (_Interaction Capability_ — Proteção contra Erros e Autodescritividade). |
| **ISO/IEC 25019:2023** (_Quality-in-Use Model_)       | Modelo de Qualidade em Uso     | Avaliação da **Eficácia** e **Eficiência** em contexto de uso escolar real (tempo de tarefa e sucesso de primeira tentativa no diário e na matrícula).                                                                                                                                                                                                    |
| **ISO/IEC 25040:2024** (_Quality Evaluation Process_) | Processo de Avaliação          | Ciclo estruturado em 5 atividades (Requisitos, Especificação, Desenho, Execução e Julgamento).                                                                                                                                                                                                                                                            |
| **Metodologia GQM** (_Goal-Question-Metric_)          | Derivação de Métricas          | Desdobramento formal em 4 objetivos, 14 questões, 15 famílias e 17 linhas operacionais (M7a/b e M14a/b desdobradas), com 3 Gates Binários eliminatórios.                                                                                                                                                                                                  |
| **Framework PSM/CID**                                 | Gestão de Recursos e Custos    | Rastreamento de métricas de processo, custos financeiros e esforço dedicado da equipe.                                                                                                                                                                                                                                                                    |

---

## 4. Projeto e Métodos de Coleta da Avaliação (Fase 3 — ISO/IEC 25040:2024)

O plano de medição e projeto da avaliação compreende a extração estática e dinâmica das métricas diretamente do software avaliado:

- **Gates Binários de Confiabilidade**: Verificação determinística de notas (`M3`) e atomicidade transacional em operações de notas e matrícula (`M4`).
- **Métricas de Manutenibilidade**: Coleta de complexidade ciclomática ($P_{90}$ e máxima), atrito de dados (`IFDL`) e índice de manutenibilidade (`MI`).
- **Testabilidade de Domínio**: Auditoria de cobertura comportamental e detecção de testes desativados com `markTestSkipped()`.
- **Agregação e Julgamento**: Modelo de agregação multicritério para cálculo do Índice por Característica ($\text{IQC}_k$) e Índice Global ($\text{IQM}$).

---

## 5. Estrutura e Mapa de Documentação do Projeto

| Artefato Documental                         | Caminho no Repositório                                                                                                             | Conteúdo Principal                                                                                                                                                    |
| :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Planejamento do Ponto de Controle 1**     | [`docs/relatorio_de_planejamento_ponto_de_controle_1_i_educar.md`](docs/relatorio_de_planejamento_ponto_de_controle_1_i_educar.md) | Linha do tempo (M0 a M5), requisitos da Fase 1, matriz de priorização ($C = I \times R$), resumo GQM e estrutura de slides.                                           |
| **Framework GQM de Avaliação (v2.0)**       | [`docs/gqm_evaluation_framework.md`](docs/gqm_evaluation_framework.md)                                                             | Objeto de avaliação, árvores GQM por característica, fórmulas matemáticas (M1 a M15), limiares e regras de decisão.                                                   |
| **Visão do Produto i-Educar**               | [`docs/agents/project_overview.md`](docs/agents/project_overview.md)                                                               | Descrição do sistema avaliado, finalidade social, partes interessadas e relação com a avaliação.                                                                      |
| **Arquitetura do i-Educar**                 | [`docs/agents/architecture.md`](docs/agents/architecture.md)                                                                       | Arquitetura híbrida (Laravel 13 e núcleo legado), papel do `LegacyController`, versões verificadas (PHP 8.5, PostgreSQL 18), módulos avaliados e esquemas PostgreSQL. |
| **Gestão de Milestones, Issues e Releases** | [`docs/gestao_projeto_releases_milestones_issues.md`](docs/gestao_projeto_releases_milestones_issues.md)                           | Alocação de custos PSM/CID, diagrama de marcos, catálogo atômico das Issues #01 a #19 e especificação das Releases E1 e E2.                                           |
| **Guia de Contribuição e Governança Git**   | [`CONTRIBUTING.md`](CONTRIBUTING.md)                                                                                               | Fluxo de trabalho de issues, branches, padrão de commits e política de revisão por pares.                                                                             |

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

Durante a preparação da Entrega 1, ferramentas de inteligência artificial apoiaram a organização da documentação, o desenvolvimento da GitPage, a apresentação de slides e a elaboração do artigo. As declarações abaixo relacionam o uso informado por cada integrante à sua participação no trabalho. A descrição das tarefas e a descrição do apoio de IA são apresentadas separadamente para registrar o papel de cada ferramenta.

### 7.1 Ítalo Alves Sampaio de Oliveira

- **Participação no trabalho:** contextualização do i-Educar e descrição da arquitetura; identificação de stakeholders e relação com os ODS 4 e 16; especificação GQM de Confiabilidade e Manutenibilidade. Essas frentes estão relacionadas às tarefas #02, #03, #06 e #07 do [catálogo de tarefas](docs/gestao_projeto_releases_milestones_issues.md).
- **Ferramenta utilizada:** OpenCode, com agentes organizados para tarefas específicas.
- **Apoio de IA declarado:** auxílio ao desenvolvimento da GitPage e à preparação de alterações na documentação, com separação das atividades por tarefa. Ítalo revisou as sugestões e implementou as alterações pertinentes ao trabalho.

### 7.2 Gabriel Barbaceli

- **Participação no trabalho:** propósito e uso pretendido da avaliação, matriz de priorização, especificação GQM de Compatibilidade e de Capacidade de Interação/Qualidade em Uso e atualização do quadro de integrantes. Essas frentes correspondem às tarefas #05, #08, #17 e #19 do [catálogo de tarefas](docs/gestao_projeto_releases_milestones_issues.md).
- **Ferramenta utilizada:** Claude.
- **Apoio de IA declarado:** refinamento dos textos da GitPage, identificação de inconsistências entre informações e apoio à revisão de problemas de escrita. As sugestões foram examinadas e ajustadas ao conteúdo da documentação.

### 7.3 Fábio Santos Araujo

- **Participação no trabalho:** elaboração do artigo, preparação dos slides e melhorias na apresentação visual da GitPage, relacionadas às tarefas #13, #14 e #18 do [catálogo de tarefas](docs/gestao_projeto_releases_milestones_issues.md).
- **Ferramenta utilizada:** GitHub Copilot.
- **Apoio de IA declarado:** auxílio aos ajustes de HTML e CSS da GitPage para melhorar a visualização das informações, refinamento dos slides e implementação das melhorias solicitadas nas revisões.

### 7.4 Arthur Soares Parente

- **Participação no trabalho:** estruturação da GitPage, organização dos documentos e preparação de templates, com relação às tarefas #01 e #18 do [catálogo de tarefas](docs/gestao_projeto_releases_milestones_issues.md).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA declarado:** refinamento da documentação técnica e apoio à organização e estruturação da GitPage, buscando clareza e coerência na apresentação dos artefatos do projeto.

### 7.5 Gustavo Silva Rodrigues

- **Participação no trabalho:** adaptação do modelo de qualidade e delimitação do escopo da avaliação, desenvolvimento e revisão do artigo, relacionados às tarefas #04 e #13 do [catálogo de tarefas](docs/gestao_projeto_releases_milestones_issues.md).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA declarado:** auxílio à escrita e à estruturação do artigo em LaTeX, à formulação e apresentação de equações, à identificação de inconsistências e à análise de referências das normas ISO para adequar o modelo de qualidade ao i-Educar. As sugestões apoiaram a articulação entre o contexto do software, as características selecionadas e a especificação da avaliação.

### 7.6 Revisão humana e responsabilidade pelo conteúdo

As sugestões foram revisadas e adaptadas pela equipe ao contexto do trabalho. Os integrantes mantêm a responsabilidade pelas decisões metodológicas, pela conferência das informações e pelo conteúdo apresentado no artigo e na GitPage. O uso de IA não substitui a consulta às fontes nem a verificação das definições, fórmulas e critérios utilizados.
