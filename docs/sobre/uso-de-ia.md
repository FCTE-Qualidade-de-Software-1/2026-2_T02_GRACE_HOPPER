# Declaração de Uso de Inteligência Artificial (Critério AG-C3)

Em cumprimento às diretrizes de integridade e transparência acadêmica da disciplina **Qualidade de Software 1 (FGA0315 — Critérios F1-C10, F2-C9 e AG-C3)**, esta página documenta as ferramentas de Inteligência Artificial generativa utilizadas como apoio durante o projeto, as tarefas em que atuaram, a declaração individual de cada integrante e o protocolo de revisão humana.

!!! important "Princípio de Autoria e Responsabilidade Técnica"
    Nenhuma ferramenta de IA substituiu a consulta direta ao código-fonte do **i-Educar 2.12**, às normas **ISO/IEC 25000 (SQuaRE)** ou aos registros do repositório no GitHub. A equipe avaliadora mantém responsabilidade integral pelas decisões metodológicas, pela definição das equações, pesos e limiares do GQM e pela veracidade de todos os dados reportados.

---

## 1. Quadro Consolidado de Ferramentas, Tarefas e Verificações

**Tabela 1 — Uso de ferramentas de IA, tarefas apoiadas e limites de verificação humana**

| Ferramenta | Tarefa Apoiada | Período | Verificações Humanas e Limites de Uso |
| :--- | :--- | :---: | :--- |
| **OpenCode** | Apoio ao desenvolvimento da GitPage e preparação de alterações na documentação com agentes organizados por tarefa | Out. 2026 | Sugestões revisadas e adaptadas ao contexto do projeto antes da implementação; todas as decisões metodológicas permaneceram sob responsabilidade da equipe. |
| **Claude** | Refinamento textual da GitPage, identificação de inconsistências terminológicas entre seções e revisão de clareza da escrita | Out. 2026 | Sugestões examinadas manualmente frente às definições do grupo; revisão humana integral do conteúdo publicado. |
| **GitHub Copilot** | Ajustes de estruturação HTML/CSS da GitPage, refinamento dos slides da apresentação PC1/PC2 e apoio na redação do manuscrito no VS Code | Out.–Nov. 2026 | A ferramenta não executou a avaliação do i-Educar nem gerou resultados experimentais. Alterações revisadas contra o framework GQM e os registros do GitHub. |
| **Gemini, Claude e Codex** | Estruturação da GitPage, formatação de equações em LaTeX/MathJax, apoio à codificação dos scripts coletores (`scripts/avaliacao/`, `scripts/evaluate-quality.php`), geração dos slides PC2 e conferência das memórias de cálculo da Fase 5 | Out.–Nov. 2026 | Conferência manual das fórmulas, pesos, limiares, saídas brutas em `evidencias/` e referências normativas ISO/IEC pela equipe; nenhum dado de medição foi sintetizado ou arbitrado por IA. |

*Fonte: Registro do projeto e declarações das Entregas 1 e 2.*

---

## 2. Declaração Individual por Integrante (Entregas 1 e 2)

Abaixo estão discriminadas as frentes de trabalho de cada membro nas Entregas 1 e 2 e a forma como as ferramentas de apoio foram utilizadas e supervisionadas:

### 2.1. Arthur Soares Parente (`23/2036770`)
- **Participação no trabalho:** Na Entrega 1, infraestrutura do repositório, automação da GitPage, limiares, planejamento Docker/AST/TCLE e Release E1 (Issues `#01`, `#09`, `#10`, `#11`, `#12`, `#15`, `#16` e `#18`). Na Entrega 2, medição de acoplamento (`M8 — DSPM`), fricção legado-moderno (`M9 — IFDL`), testes ativos com asserção (`M11 — TTAE`), proteção contra erros do usuário (`Gate M12 — IPPE`) e autodescritividade de mensagens (`M13 — ADMV`) (Issues `#44` e `#45`, PR `#55`).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA e revisão humana:** Apoio na automação dos scripts de extração estática e de submissão dos 12 cenários negativos contra o container do i-Educar, além da formatação dos relatórios em Markdown. Todas as consultas SQL, capturas HTTP e contagens de JUnit XML foram verificadas manualmente.

### 2.2. Fábio Santos Araujo (`22/2022082`)
- **Participação no trabalho:** Na Entrega 1, estruturação do artigo científico no template IEEE, apresentação de slides PC1 e melhorias na GitPage (Issues `#13`, `#14` e `#18`). Na Entrega 2, consolidação da Fase 5 (cálculo dos índices $\text{IQC}_k$, análise do status suspenso de $\text{IQM}$ e cenários de sensibilidade, verificação dos Gates Binários, enquadramento de release e parecer técnico por stakeholder), elaboração da apresentação final PC2 (`apresentacao_pc2.pptx` e `apresentacao_pc2.pdf`), auditoria de horas e custos PSM/CID (`Medição 3`) e preparação da Release E2 (`v2.0.0-pc2`) (Issues `#47` e `#49`).
- **Ferramentas utilizadas:** GitHub Copilot e Gemini (Antigravity).
- **Apoio de IA e revisão humana:** Apoio na conferência algébrica das memórias de cálculo de $\text{IQC}_k$ e $\text{IQM}$, geração programática dos slides PC2 (`python-pptx` e PDF) e reconciliação automatizada de metadados das issues via GitHub CLI. Todos os números, equações e pareceres foram auditados contra as evidências brutas da Fase 4.

### 2.3. Gabriel Barbaceli (`21/1045122`)
- **Participação no trabalho:** Na Entrega 1, definição do propósito, matriz de priorização ($C = I \times R$), especificação GQM de `G1` e `G4` e quadro de integrantes (Issues `#05`, `#08`, `#17` e `#19`). Na Entrega 2, evolução e execução do motor estático AST (`M7a`, `M7b`, `M10`), formalização da regra de contingência para `M14a/b` e `M15` e execução da Ação de Melhoria sobre `getSituacaoNotas` com 50.000 testes de equivalência (Issues `#43`, `#46` e `#56`, PRs `#53` e `#57`).
- **Ferramenta utilizada:** Claude.
- **Apoio de IA e revisão humana:** Apoio na escrita do parser AST em PHP, do arnês de teste diferencial de equivalência e na redação técnica dos relatórios da GitPage. O patch de refatoração e os resultados de equivalência foram integralmente validados por execução real.

### 2.4. Gustavo Silva Rodrigues (`23/2036887`)
- **Participação no trabalho:** Na Entrega 1, adaptação do modelo ISO/IEC 25010:2023, delimitação do escopo e coautoria do artigo (Issues `#04` e `#13`). Na Entrega 2, construção do manifesto congelado de 30 cenários do oráculo pedagógico e execução da bateria determinística do `Gate M3 (DCNM = 100%)` sobre `Boletim.php`, além da consolidação do Artigo v2 (Issues `#40` e `#48`, PR `#54`).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA e revisão humana:** Apoio na estruturação do runner de testes PHPUnit do oráculo (`M3OracleTest.php`), consolidação dos logs JSON/JUnit e formatação em LaTeX. Todas as regras pedagógicas e asserções foram conferidas sobre o código-fonte do i-Educar 2.12.

### 2.5. Ítalo Alves Sampaio de Oliveira (`23/2037937`)
- **Participação no trabalho:** Na Entrega 1, contextualização arquitetural do i-Educar, mapeamento de stakeholders, ODS 4/16 e GQM de `G2` e `G3` (Issues `#02`, `#03`, `#06` e `#07`). Na Entrega 2, provisionamento do ambiente Docker do i-Educar 2.12, ensaio de coexistência de instâncias (`M1 — TINCR = 100%`) e validação contratual JSON Schema dos 10 endpoints REST (`M2 — CEI = 90%`) (Issues `#38` e `#39`, PR `#52`).
- **Ferramentas utilizadas:** OpenCode e Claude.
- **Apoio de IA e revisão humana:** Auxílio na elaboração dos scripts `m1_coexistencia.sh` e `m2_cei.py`, derivação dos JSON Schemas a partir dos controllers e documentação das ameaças à validade. Todos os testes foram executados em containers reais e auditados pelo autor.

### 2.6. Ricardo Lucas Winchello Vieira Branco (`22/1008409`)
- **Participação no trabalho:** Na Entrega 1, revisão técnica cruzada da GitPage e validação do artigo frente às rubricas da disciplina. Na Entrega 2, designado para a trilha de confiabilidade complementar (`Issues #41` e `#42`) e revisão de conformidade documental.
- **Supervisão e revisão humana:** Conferência independente de links, numeração de tabelas/figuras, somas percentuais de esforço e aderência entre os números reportados na GitPage e nas apresentações.

---

## 3. Identidade Visual e Créditos de Mídia

- **Fotografia histórica de Grace Hopper:** Retrato oficial da Marinha dos Estados Unidos (*Commodore Grace M. Hopper, USN, covered*), fotógrafo James S. Davis (20 de janeiro de 1984), em domínio público nos termos de obras do Governo Federal dos EUA, obtido via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Commodore_Grace_M._Hopper,_USN_(covered)_head_and_shoulders_crop.jpg).
- **Logo e Favicon (`grace-hopper-logo.svg`):** Arte vetorial autoral em SVG desenvolvida para o repositório da equipe em referência à estrela naval e às chaves de compilação `{ GH }`.
