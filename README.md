# Avaliação de Qualidade de Software — i-Educar (`projeto-qualidade`)

[![Norma ISO/IEC 25010:2023](https://img.shields.io/badge/Norma-ISO%2FIEC%2025010%3A2023-blue.svg)](https://www.iso.org/standard/78176.html)
[![Norma ISO/IEC 25040:2024](https://img.shields.io/badge/Processo-ISO%2FIEC%2025040%3A2024-green.svg)](https://www.iso.org/standard/83642.html)
[![Metodologia GQM](https://img.shields.io/badge/Metodologia-GQM%20v2.0-orange.svg)](docs/gqm_evaluation_framework.md)
[![Status da Release](https://img.shields.io/badge/Release-E1%20(v1.0.0--pc1)-purple.svg)](docs/gestao_projeto_releases_milestones_issues.md)
[![Documentação GitHub Pages](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/)

Este repositório abriga o projeto de avaliação de qualidade de software do sistema livre de gestão escolar **i-Educar**, desenvolvido no âmbito da disciplina **Qualidade de Software 1 (FGA0315)** da **Universidade de Brasília (UnB / FGA)** no semestre letivo **2026.2**.

---

## 1. Identificação da Equipe e Gestão de Recursos (PSM/CID — Critério AG-C5)

A tabela abaixo registra os membros da equipe avaliadora, com campos reservados para identificação individual, papel, valor/hora de trabalho e esforço planejado para o **Ponto de Controle 1 (Entrega 1)**.

| Integrante | Matrícula UnB | Usuário GitHub | Papel Principal | Horas (h) | Valor / Hora | Custo Total | % Esforço |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | `23/2036770` | `@ArthurDevWorks` | Gestor de Configuração / GitPage | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Fábio Santos Araujo** | `22/2022082` | `@fabiofonteles1` | Redação do Artigo (Overleaf) | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gabriel Barbaceli** | `21/1045122` | `@Nibaacriba` | GitPage / Especificação GQM (Compatibilidade e Capacidade de Interação) | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gustavo Silva Rodrigues** | `23/2036887` | `@g-srodrigues` | Analista de Qualidade / Modelo ISO/IEC 25010 e Escopo | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | `23/2037937` | `@ItaloSamP` | Analista do Produto e Stakeholders / GitPage | 12h | R$ 50,00 | R$ 600,00 | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | `22/1008409` | `@ChickRicks` | Redação do Artigo (Overleaf) | 12h | R$ 50,00 | R$ 600,00 | **16,66%** |
| **TOTAL CONSOLIDADO** | — | — | **Esforço Acumulado — Ponto de Controle 1** | **72h** | **R$ 50,00** | **R$ 3.600,00** | **100%** |

*Nota: O esforço foi dividido igualmente entre os 6 integrantes (1/6 cada); os centésimos foram ajustados para que a soma seja exatamente 100%. Horas e custos devem ser atualizados conforme o andamento das issues associadas.*

---

## 2. Objeto de Avaliação e Escopo Tecnológico

O software avaliado é o **i-Educar** (versão 2.12.0 / repositório base `portabilis/i-educar`), um monólito híbrido que articula um núcleo legado em PHP (`ieducar/`) a uma infraestrutura moderna em Laravel 13 com banco de dados relacional PostgreSQL.

A avaliação concentra-se em dois módulos funcionais de alta criticidade:
1. **Módulo de Matrícula de Alunos**: Vínculo formal (`pmieducar.matricula`), enturmação e remanejamento (`pmieducar.matricula_turma`), ciclo de vida de situações escolares (`RegistrationStatus`) e operações de cancelamento atômico (`RegistrationService`).
2. **Módulo de Lançamento de Notas e Menções**: Regras pedagógicas configuráveis (`modules.regra_avaliacao`), tabelas dinâmicas de menção e arredondamento (`modules.tabela_arredondamento_valor`), controle do diário eletrônico (`DiarioController` e `DiarioApiController`) e motor de médias (`Avaliacao_Service_Boletim`).

---

## 3. Fundamentação Normativa e Metodológica

A avaliação é conduzida seguindo estritamente as normas internacionais vigentes e frameworks de engenharia:
- **ISO/IEC 25010:2023** (*Product Quality Model*): 4 características recortadas:
  - **Compatibilidade** (Coexistência de Recursos e Interoperabilidade de Dados)
  - **Confiabilidade** (Ausência de Falhas / *Faultlessness*, Tolerância a Falhas e Recuperabilidade)
  - **Manutenibilidade** (Modularidade, Analisabilidade, Modificabilidade e Testabilidade)
  - **Capacidade de Interação** (*Interaction Capability* — Proteção contra Erros do Usuário e Autodescritividade)
- **ISO/IEC 25019:2023** (*Quality-in-Use Model*): Avaliação da Eficácia e Eficiência em contexto de uso escolar real (tempo de tarefa e sucesso de primeira tentativa no diário).
- **ISO/IEC 25040:2024** (*Quality Evaluation Process*): Ciclo estruturado em 5 atividades (Requisitos, Especificação, Desenho, Execução e Julgamento).
- **Metodologia GQM (Goal-Question-Metric)**: Desdobramento formal em 15 métricas quantitativas com 3 Gates Binários eliminatórios de integridade.
- **Framework PSM/CID**: Rastreamento de métricas de processo, custos financeiros e esforço dedicado da equipe.

---

## 4. Projeto e Métodos de Coleta da Avaliação (Fase 3 — ISO/IEC 25040:2024)

O plano de medição e projeto da avaliação compreende a extração estática e dinâmica das métricas diretamente do software avaliado:
- **Gates Binários de Confiabilidade**: Verificação determinística de notas (M3) e atomicidade transacional em operações de notas e matrícula (M4).
- **Métricas de Manutenibilidade**: Coleta de complexidade ciclomática (P90 e máxima), atrito de dados (IFDL) e índice de manutenibilidade (MI).
- **Testabilidade de Domínio**: Auditoria de cobertura comportamental e detecção de testes desativados com `markTestSkipped()`.
- **Agregação e Julgamento**: Modelo de agregação multicritério para cálculo do Índice por Característica ($IQC_k$) e Índice Global ($IQM$).

---

## 5. Estrutura e Mapa de Documentação do Projeto

- **Planejamento do Ponto de Controle 1**: [`docs/relatorio_de_planejamento_ponto_de_controle_1_i_educar.md`](docs/relatorio_de_planejamento_ponto_de_controle_1_i_educar.md)
- **Gestão de Milestones, Issues e Releases**: [`docs/gestao_projeto_releases_milestones_issues.md`](docs/gestao_projeto_releases_milestones_issues.md)
- **Framework GQM de Avaliação de Qualidade (v2.0)**: [`docs/gqm_evaluation_framework.md`](docs/gqm_evaluation_framework.md)
- **Guia de Contribuição e Governança Git**: [`CONTRIBUTING.md`](CONTRIBUTING.md)

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
   *(O script executa `mkdocs build --strict` e valida títulos, links e fórmulas renderizadas).*

---

## 7. Governança e Declaração de Uso de Ferramentas de IA (Critério AG-C3)

Em conformidade com os critérios de transparência acadêmica da disciplina FGA0315:
- **Ferramentas de IA Utilizadas**: Este repositório utilizou assistentes de IA baseados em modelos avançados (Google Gemini / Anthropic Claude) via plataforma Antigravity para apoio em inspeção estática, geração de scaffolds de documentação e formulação de templates.
- **Supervisão Humana**: Todo o conteúdo conceitual, mapeamento de normas (ISO 25010/25019/25040), equações matemáticas e julgamentos técnicos foram integralmente revisados, calibrados e validados tecnicamente pelos integrantes da equipe.
- **Rigor Editorial**: O repositório e os artefatos acadêmicos observam rigor formal estrito, sem inclusão de emojis decorativos ou textos não rastreáveis.
