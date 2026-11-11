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
| **GitHub Copilot** | Ajustes de estruturação HTML/CSS da GitPage, refinamento dos slides da apresentação PC1 e apoio na redação do manuscrito no VS Code | Out. 2026 | A ferramenta não executou a avaliação do i-Educar nem gerou resultados experimentais. Alterações revisadas contra o framework GQM e os registros do GitHub. |
| **Gemini e Codex** | Estruturação e modularização da GitPage, formatação de equações em LaTeX/MathJax, scripts de automação e conferência de aderência às rubricas | Out.–Nov. 2026 | Conferência manual das fórmulas, pesos, limiares e referências normativas ISO/IEC pela equipe; o apoio não substitui a leitura das fontes primárias. |

*Fonte: Registro do projeto e seção de Declaração de Uso de IA do artigo científico da Entrega 1.*

---

## 2. Declaração Individual por Integrante

Abaixo estão discriminadas as frentes de trabalho de cada membro e a forma como as ferramentas de apoio foram utilizadas e supervisionadas:

### 2.1. Arthur Soares Parente (`23/2036770`)
- **Participação no trabalho:** Infraestrutura do repositório, automação e arquitetura da GitPage; formulação matemática dos limiares e regras de decisão; planejamento do ambiente Docker, do motor de análise estática PHP e do protocolo experimental de usabilidade (TCLE); auditoria preventiva das rubricas e publicação da Release E1 (Issues `#01`, `#09`, `#10`, `#11`, `#12`, `#15`, `#16` e `#18`).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA e revisão humana:** Apoio na estruturação e automação das páginas em MkDocs Material, estilização CSS, conferência de consistência das especificações do ambiente Docker e auditoria documental frente às rubricas. Todas as configurações, scripts e fórmulas foram testados e validados localmente antes do commit.

### 2.2. Fábio Santos Araujo (`22/2022082`)
- **Participação no trabalho:** Elaboração e estruturação do artigo científico no template IEEE, preparação dos slides da apresentação do Ponto de Controle 1 e melhorias na apresentação visual da GitPage (Issues `#13`, `#14` e `#18`).
- **Ferramenta utilizada:** GitHub Copilot.
- **Apoio de IA e revisão humana:** Auxílio em ajustes de HTML/CSS da GitPage, refinamento da estrutura de slides e revisão de clareza no artigo em LaTeX. Todas as tabelas e citações foram conferidas manualmente contra os documentos-fonte da equipe.

### 2.3. Gabriel Barbaceli (`21/1045122`)
- **Participação no trabalho:** Definição do propósito e uso pretendido da avaliação, matriz de priorização ($C = I \times R$), especificação GQM de Compatibilidade (`G1`) e de Capacidade de Interação/Qualidade em Uso (`G4`), e sincronização do quadro de integrantes (Issues `#05`, `#08`, `#17` e `#19`).
- **Ferramenta utilizada:** Claude.
- **Apoio de IA e revisão humana:** Refinamento da redação técnica na GitPage, detecção de eventuais divergências entre tabelas e revisão gramatical. As métricas, hipóteses e limiares foram definidos e validados pelo autor.

### 2.4. Gustavo Silva Rodrigues (`23/2036887`)
- **Participação no trabalho:** Adaptação do modelo de qualidade da ISO/IEC 25010:2023, delimitação do escopo da avaliação e coautoria/revisão do artigo científico em LaTeX (Issues `#04` e `#13`).
- **Ferramentas utilizadas:** Gemini e Codex.
- **Apoio de IA e revisão humana:** Apoio à estruturação do artigo em LaTeX, formatação tipográfica de equações e verificação de consistência terminológica da edição 2023 da ISO/IEC 25010. Todo o conteúdo foi confrontado com o escopo real do i-Educar.

### 2.5. Ítalo Alves Sampaio de Oliveira (`23/2037937`)
- **Participação no trabalho:** Contextualização do i-Educar e mapeamento da arquitetura híbrida; identificação das partes interessadas e alinhamento aos ODS 4 e 16; especificação GQM de Confiabilidade (`G2`) e Manutenibilidade (`G3`) (Issues `#02`, `#03`, `#06` e `#07`).
- **Ferramenta utilizada:** OpenCode (com agentes organizados por tarefa).
- **Apoio de IA e revisão humana:** Auxílio na organização dos arquivos de documentação da GitPage e formatação das árvores e tabelas GQM. Ítalo revisou todas as sugestões contra a base de código do `portabilis/i-educar`.

### 2.6. Ricardo Lucas Winchello Vieira Branco (`22/1008409`)
- **Participação no trabalho:** Revisão técnica cruzada da GitPage e validação de conformidade do artigo científico frente aos critérios de avaliação da disciplina.
- **Supervisão e revisão humana:** Conferência independente de links, numeração de tabelas/figuras, somas percentuais de esforço e aderência entre os números reportados na GitPage e no PDF do artigo.

---

## 3. Identidade Visual e Créditos de Mídia

- **Fotografia histórica de Grace Hopper:** Retrato oficial da Marinha dos Estados Unidos (*Commodore Grace M. Hopper, USN, covered*), fotógrafo James S. Davis (20 de janeiro de 1984), em domínio público nos termos de obras do Governo Federal dos EUA, obtido via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Commodore_Grace_M._Hopper,_USN_(covered)_head_and_shoulders_crop.jpg).
- **Logo e Favicon (`grace-hopper-logo.svg`):** Arte vetorial autoral em SVG desenvolvida para o repositório da equipe em referência à estrela naval e às chaves de compilação `{ GH }`.
