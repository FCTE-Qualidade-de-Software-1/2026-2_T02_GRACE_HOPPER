# Relatório de Planejamento e Acompanhamento — Ponto de Controle 1 (Entrega 1)

**Disciplina:** Qualidade de Software 1 (FGA0315)

**Objeto de Avaliação:** i-Educar (`https://github.com/portabilis/i-educar`)

**Normas Base:** ISO/IEC 25010 (Modelo de Qualidade) e ISO/IEC 25040 (Processo de Avaliação)

---

## 1. Linha do Tempo e Ponto Atual do Projeto (Calendário e Progresso — PSM/CID)

Esta seção substitui a exibição de trechos soltos do artigo, permitindo que a professora acompanhe visualmente a evolução do trabalho, o estágio atual da equipe e o encadeamento das entregas até a **Release E1**.

| Marco (Milestone) | Etapa / Período Relativo | Fase / Entregável Relacionado | Descrição das Atividades | Status Atual |
| :--- | :--- | :--- | :--- | :--- |
| **M0: Setup Inicial** | Etapa 1 | Concepção e Infraestrutura | Definição do grupo, escolha do software livre **i-Educar**, criação do repositório Git, configuração de *Issues/Milestones* e estrutura base da GitPage. | **CONCLUÍDO** |
| **M1: Requisitos da Avaliação** | Etapa 2 | **Fase 1 (ISO/IEC 25040)** | Definição do propósito da avaliação, identificação de *stakeholders*, adaptação gráfica do modelo de qualidade, justificativa das 4 características (Compatibilidade, Confiabilidade, Manutenibilidade e Usabilidade), definição de escopo/profundidade e alinhamento aos ODS da ONU. | **ONDE ESTAMOS (Ponto de Controle 1)** |
| **M2: Especificação da Avaliação** | Etapa 3 | **Fase 2 (ISO/IEC 25040)** | Construção das árvores GQM (*Goal-Question-Metric*) para as 4 características selecionadas, definição das métricas, fórmulas de cálculo, níveis de pontuação (limiares numéricos) e critérios de julgamento. | **EM ANDAMENTO (Próximo Passo Imediato)** |
| **M3: Projeto da Avaliação** | Etapa 4 | **Fase 3 (ISO/IEC 25040)** | Seleção das ferramentas de análise e teste (SonarQube, Postman, Lighthouse, TCLE), definição do ambiente Docker do i-Educar, planejamento de coleta e cronograma de execução. | **PLANEJADO** |
| **M4: Consolidação, Slides e Release E1** | Etapa 5 (Marco da Entrega 1) | **GitPage + Artigo v1 + Slides PC1 + Release 1** | Redação da 1ª versão do artigo (Introdução, Referencial Teórico, Metodologia, Fases 1 a 3), atualização da GitPage, elaboração dos slides do Ponto de Controle 1, Tabela de Contribuição/Custos e publicação da *Tag/Release E1*. | **PLANEJADO** |
| **M5: Execução e Conclusão** | Etapa Final (Pós-Entrega 1) | **Fase 4 (ISO/IEC 25040) + Entrega 2** | Ajustes apontados pela professora no PC1, coleta de dados brutos, logs e vídeos no i-Educar (Fase 4), análise dos resultados e conclusão da 2ª versão do artigo (*Release E2*). | **FUTURO (Entrega 2)** |

---

## 2. Detalhamento das Fases a Desenvolver até o Ponto de Controle 1

De acordo com o documento da disciplina, o planejamento até o primeiro ponto de controle estrutura as bases do processo de avaliação (ISO/IEC 25040), além da **Gestão do Projeto (PSM/CID)**, **GitPage**, **1ª Versão do Artigo** e **Apresentação de Slides**. Abaixo está o guia completo do que deve constar em cada etapa.

### 2.1. Fase 1: Estabelecer os Requisitos da Avaliação

Para garantir pontuação máxima na rubrica da Fase 1, a equipe deve documentar na GitPage e no Artigo os seguintes subitens:

1. **Contextualização do Produto (i-Educar):**
   * Sistema de Gestão Escolar *open source* desenvolvido originalmente em PHP e modernizado com o *framework* Laravel, mantido pela comunidade e pela Portabilis.
   * Gerencia matrículas, turmas, enturmações, diários de classe, lançamento de notas/frequências, emissão de históricos e exportação direta para o Censo Escolar (Educacenso/INEP).

2. **Propósito da Avaliação e Uso Pretendido:**
   * **Propósito:** Avaliar a qualidade interna, externa e em uso da versão atual do i-Educar para diagnosticar pontos críticos de arquitetura, estabilidade, integração e interface.
   * **Uso Pretendido:** Fornecer um parecer técnico estruturado para Secretarias Municipais de Educação (que desejam implantar ou atualizar o sistema) e para a comunidade de desenvolvedores (orientando refatorações prioritárias).

3. **Identificação do Requisitante e Partes Interessadas (Stakeholders):**
   * **Requisitante / Mantenedor:** Comunidade i-Educar, Portabilis e equipes de TI das prefeituras.
   * **Usuários Finais Primários:** Secretários escolares, diretores, coordenadores pedagógicos e professores da rede pública.
   * **Usuários Secundários / Integradores:** Analistas de sistemas municipais responsáveis pela integração via API e envio de dados ao MEC/INEP.

4. **Seleção, Priorização e Adaptação do Modelo de Qualidade (ISO/IEC 25010):**
   * **Importante:** Elaborar um **diagrama próprio** (representação gráfica adaptada da ISO/IEC 25010) destacando apenas as **4 características** e as respectivas **subcaracterísticas** recortadas para o i-Educar:
     * **Usabilidade** (Característica obrigatória / foco em interação): *Apreensibilidade*, *Operabilidade*, *Proteção contra erros do usuário* e *Acessibilidade*. Justificativa: perfil heterogêneo de letramento digital dos servidores escolares e necessidade de evitar erros de preenchimento cadastral.
     * **Compatibilidade** (1ª característica adicional): *Coexistência* e *Interoperabilidade*. Justificativa: dependência obrigatória de troca de dados com o sistema Educacenso (INEP) e integração via API REST com sistemas municipais.
     * **Confiabilidade** (2ª característica adicional): *Maturidade*, *Disponibilidade* e *Tolerância a falhas*. Justificativa: alta criticidade durante períodos de matrícula e fechamento de bimestres letivos; falhas nesses períodos paralisam a gestão escolar municipal.
     * **Manutenibilidade** (3ª característica adicional): *Modularidade*, *Analisabilidade*, *Modificabilidade* e *Testabilidade*. Justificativa: coexistência de código legado (`ieducar/intranet`) com código moderno em Laravel (`app/`), exigindo facilidade de manutenção para adaptar regras de avaliação específicas de cada município.

5. **Escopo, Profundidade e Objetos de Avaliação (O que entra e o que fica de fora):**
   * **Dentro do Escopo (Objetos Avaliados):** Fluxos centrais de cadastro escolar e matrícula (Usabilidade), *endpoints* da API REST e módulo de integração/exportação (Compatibilidade), tratamento de exceções e histórico de defeitos/testes nos módulos centrais (Confiabilidade), e análise estática dos diretórios `app/` e módulos principais do repositório `portabilis/i-educar` (Manutenibilidade).
   * **Fora do Escopo (e Por Quê):** Avaliação de *Performance/Eficiência de Desempenho* sob estresse de múltiplos municípios simultâneos (pois exigiria infraestrutura de nuvem equivalente à produção de grandes prefeituras) e pacotes de terceiros/bibliotecas externas na pasta `vendor/` (avaliaremos apenas o código de responsabilidade direta do projeto i-Educar).

6. **Relação com os Objetivos de Desenvolvimento Sustentável (ODS da ONU):**
   * **ODS 4 — Educação de Qualidade:**
     * *Meta 4.1 e Meta 4.a:* Garantir educação primária e secundária de qualidade e melhorar a gestão dos ambientes escolares.
     * *Justificativa e Indicadores:* O i-Educar reduz a evasão escolar e melhora a alocação de recursos públicos ao automatizar o controle de frequência, notas e o reporte fidedigno ao Censo Escolar.
   * **ODS 16 — Paz, Justiça e Instituições Eficazes:**
     * *Meta 16.6:* Desenvolver instituições eficazes, responsáveis e transparentes em todos os níveis.
     * *Justificativa:* Por ser um Bem Público Digital (*Digital Public Good*) em código aberto, promove transparência administrativa e economia de recursos públicos em centenas de municípios brasileiros.

---

### 2.2. Fase 2: Especificar a Avaliação (GQM e Critérios de Julgamento)

Nesta fase, a equipe transforma as 4 características em medições concretas utilizando a abordagem **GQM (Goal-Question-Metric)** e estabelece as regras matemáticas de aprovação.

#### Quadro Resumo do GQM Proposto para o i-Educar

| Característica (Subcaracterística) | Objetivo (Goal - GQM) | Questões (Questions) | Métricas e Fórmulas (Metrics) | Níveis de Pontuação e Critério de Julgamento |
| :--- | :--- | :--- | :--- | :--- |
| **Compatibilidade** (*Interoperabilidade*) | Analisar a API REST e as interfaces de troca de dados do i-Educar com o propósito de avaliar a interoperabilidade sob o ponto de vista de integradores técnicos. | **Q1:** Os *endpoints* da API possuem documentação completa de requisição e resposta?<br>**Q2:** A troca de payloads JSON segue formatos padronizados sem falhas de esquema? | **M1.1 (Cobertura de Doc API):** $X = \frac{N_{\text{endpoints doc}}}{N_{\text{total endpoints}}} \times 100$<br>**M1.2 (Conformidade de Payload):** $Y = \frac{N_{\text{respostas válidas}}}{N_{\text{testes realizados}}} \times 100$ | **Insatisfatório:** $< 60\%$<br>**Aceitável:** $60\% \text{ a } 84\%$<br>**Excelente:** $\ge 85\%$ |
| **Confiabilidade** (*Maturidade e Tolerância a Falhas*) | Analisar os fluxos críticos e o repositório do i-Educar com o propósito de avaliar a maturidade e tolerância a falhas sob o ponto de vista da gestão escolar. | **Q1:** O sistema trata entradas inválidas nos fluxos críticos sem expor erros fatais (HTTP 500)?<br>**Q2:** Qual a taxa de resolução de defeitos e cobertura de testes nos módulos centrais? | **M2.1 (Tolerância a Falhas):** $X = \frac{N_{\text{falhas tratadas}}}{N_{\text{injeções de falha}}} \times 100$<br>**M2.2 (Resolução de Bugs):** $Y = \frac{N_{\text{issues bug fechadas}}}{N_{\text{issues bug totais}}} \times 100$ | **Insatisfatório:** $< 70\%$<br>**Aceitável:** $70\% \text{ a } 89\%$<br>**Excelente:** $\ge 90\%$ |
| **Manutenibilidade** (*Analisabilidade e Modificabilidade*) | Analisar o código-fonte do repositório `portabilis/i-educar` com o propósito de avaliar a facilidade de manutenção sob o ponto de vista dos desenvolvedores. | **Q1:** Qual o nível de complexidade ciclomática e duplicação de código?<br>**Q2:** Qual a densidade de *Code Smells* e dívida técnica nos módulos avaliados? | **M3.1 (Duplicação de Código):** Percentual de linhas duplicadas ($\%$).<br>**M3.2 (Complexidade Ciclomática):** Média de caminhos independentes por método ($CC$). | **M3.1 Duplicação:** Excelente $\le 3\%$; Aceitável $3,1\% \text{ a } 7\%$; Insatisfatório $> 7\%$.<br>**M3.2 Complexidade:** Excelente $CC \le 5$; Aceitável $6 \text{ a } 10$; Insatisfatório $> 10$. |
| **Usabilidade** (*Operabilidade, Proteção contra erros e Acessibilidade*) | Analisar as telas de cadastro e matrícula do i-Educar com o propósito de avaliar a facilidade de uso e acessibilidade sob o ponto de vista dos secretários escolares. | **Q1:** Os formulários previnem erros do usuário com validações claras?<br>**Q2:** As telas principais atendem aos critérios de acessibilidade web (WCAG/eMAG)? | **M4.1 (Prevenção de Erros):** $X = \frac{N_{\text{campos com validação}}}{N_{\text{campos críticos}}} \times 100$<br>**M4.2 (Índice de Acessibilidade):** Pontuação obtida no Lighthouse / axe DevTools ($0 \text{ a } 100$). | **Insatisfatório:** $< 65\text{ pts/}\%$<br>**Aceitável:** $65 \text{ a } 84\text{ pts/}\%$<br>**Excelente:** $\ge 85\text{ pts/}\%$ |

---

### 2.3. Fase 3: Projetar a Avaliação (Plano de Avaliação e Ferramentas)

Para demonstrar planejamento completo e alinhamento com a futura execução (Fase 4), a equipe deve deixar estruturado:

1. **Ambiente de Testes e Versão do Produto:**
   * Utilização do ambiente conteinerizado oficial (`docker-compose` do repositório `portabilis/i-educar`), fixando a *tag/release* estável mais recente para garantir reprodutibilidade científica.
2. **Métodos, Instrumentos e Ferramentas de Coleta:**
   * **Manutenibilidade:** Execução de análise estática via **SonarQube / PHPMetrics** sobre os diretórios do projeto, exportando relatórios brutos (CSV/JSON/PDF).
   * **Compatibilidade e Confiabilidade:** Execução de suíte de testes de API via **Postman / Insomnia** e testes funcionais nos fluxos de matrícula, com gravação de *logs* de resposta e vídeos da execução.
   * **Usabilidade:** Inspeção automatizada de acessibilidade via **Google Lighthouse / axe DevTools** nas telas de cadastro escolar e avaliação guiada de tarefas (com preparação do Termo de Consentimento Livre e Esclarecido — TCLE, caso envolva participantes humanos).

---

## 3. Gestão de Recursos, Esforço e Custos (PSM/CID e Critério AG-C5)

Conforme solicitado pela professora e exigido pela métrica de **Recursos e Custos (PSM/CID)** e pelo critério **AG-C5 (Transparência da Contribuição Individual)**, a tabela abaixo unifica as tarefas executadas, a quantidade de horas dedicadas, o **valor por hora de cada integrante** e o **percentual de esforço (somando 100%)**.

| Integrante | Papel Principal na Equipe | Responsabilidades e Tarefas Executadas no Ponto de Controle 1 | Horas Dedicadas (h) | Valor / Hora (R$) | Custo Total (R$) | % de Esforço (AG-C5) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Integrante 1** | Gestor de Qualidade / Especialista em Compatibilidade | Estruturação da GitPage e métricas PSM/CID; mapeamento de *stakeholders* (Fase 1); especificação GQM de **Compatibilidade** (Fase 2); revisão da Introdução do artigo. | 12h | R$ 50,00 | R$ 600,00 | **25%** |
| **Integrante 2** | Analista de Arquitetura / Especialista em Manutenibilidade | Levantamento da arquitetura do repositório `portabilis/i-educar`; adaptação gráfica do modelo ISO 25010 (Fase 1); especificação GQM de **Manutenibilidade** (Fase 2); Referencial Teórico. | 12h | R$ 50,00 | R$ 600,00 | **25%** |
| **Integrante 3** | Engenheiro de Testes / Especialista em Confiabilidade | Análise de *issues* e maturidade do i-Educar; definição do propósito e escopo da avaliação (Fase 1); especificação GQM de **Confiabilidade** (Fase 2); seção de Metodologia. | 12h | R$ 50,00 | R$ 600,00 | **25%** |
| **Integrante 4** | Especialista em UX / Usabilidade | Mapeamento dos perfis de usuários escolares e alinhamento aos ODS 4 e 16 (Fase 1); especificação GQM de **Usabilidade** (Fase 2); elaboração dos slides e padronização do artigo. | 12h | R$ 50,00 | R$ 600,00 | **25%** |
| **TOTAL DA EQUIPE** | — | **Entregáveis Consolidados até o Ponto de Controle 1** | **48h** | **Média: R$ 50,00/h** | **R$ 2.400,00** | **100%** |

---

## 4. Estrutura da Apresentação de Slides para o Ponto de Controle 1

Como o objetivo da apresentação é mostrar o andamento do projeto, a linha do tempo, o ponto atual e os próximos passos (em vez de ler trechos longos do artigo), recomenda-se uma apresentação objetiva de **8 slides**:

* **Slide 1 — Capa e Identificação:**
  * Título do Projeto: *Avaliação de Qualidade do Sistema de Gestão Escolar i-Educar sob a Ótica da Família ISO/IEC 25000 (SQuaRE)*.
  * Nomes dos integrantes, link do repositório avaliado (`portabilis/i-educar`) e link da GitPage da equipe.
* **Slide 2 — Linha do Tempo e Ponto Atual ("Onde Estamos"):**
  * Exibição visual da **Tabela da Seção 1** (ou diagrama de linha do tempo) destacando os marcos concluídos (**M0**), o ponto atual (**M1/M2 — Ponto de Controle 1**) e os próximos passos até a **Release E1** e **Entrega 2**.
* **Slide 3 — Fase 1: Objeto de Estudo, Propósito e Stakeholders:**
  * Breve visão da arquitetura do **i-Educar** (PHP/Laravel), propósito da avaliação, partes interessadas (Secretarias Municipais, Portabilis, Professores/Secretários) e alinhamento com os **ODS 4 e ODS 16 da ONU**.
* **Slide 4 — Fase 1: Modelo de Qualidade Adaptado (ISO/IEC 25010) e Escopo:**
  * Apresentação do **diagrama próprio** com o recorte das 4 características (**Compatibilidade, Confiabilidade, Manutenibilidade e Usabilidade**) e suas subcaracterísticas, além do quadro "O que entra no escopo vs. O que fica de fora".
* **Slide 5 — Fase 2: Especificação GQM (Compatibilidade e Confiabilidade):**
  * Síntese visual dos Objetivos, Questões, Métricas e Critérios de Julgamento para a API/Educacenso (Compatibilidade) e Tolerância a Falhas/Maturidade (Confiabilidade).
* **Slide 6 — Fase 2: Especificação GQM (Manutenibilidade e Usabilidade):**
  * Síntese visual dos Objetivos, Questões, Métricas e Critérios de Julgamento para o Código-Fonte (Manutenibilidade) e Fluxos de Matrícula/Acessibilidade (Usabilidade).
* **Slide 7 — Gestão do Projeto (PSM/CID): Tabela de Contribuição e Custo/Hora:**
  * Apresentação da **Tabela da Seção 3** com o papel de cada integrante, horas dedicadas, **valor/hora (R$)**, custo total acumulado e percentual de esforço somando **100%**.
* **Slide 8 — Próximos Passos e Checklist de Entregáveis:**
  * Validação do GQM com a professora no Ponto de Controle 1;
  * Consolidação do Plano de Avaliação (Fase 3: Docker + SonarQube + Postman + Lighthouse);
  * Fechamento da 1ª versão do Artigo, revisão da GitPage (critério **F3-C7**) e publicação da *Release E1*.

---

## 5. Checklist de Qualidade Documental (Prevenção de Penalidades na Rubrica)

Antes de apresentar e gerar a *Release*, a equipe deve validar os seguintes critérios obrigatórios das diretrizes da disciplina:

1. **Critério AG-C3 (Zero Emojis/Figurinhas):** Verificar se a GitPage e o Artigo não possuem nenhum emoji, ícone decorativo ou figurinha no corpo do texto e nos títulos.
2. **Critério AG-C3 (Declaração de Uso de IA):** Incluir seção explícita no artigo e na GitPage informando qual ferramenta de IA foi utilizada, para quais tarefas de apoio e como a equipe revisou e validou tecnicamente todo o conteúdo gerado.
3. **Critério AG-C2 e AG-C4 (Rigor Editorial):** Garantir que todas as figuras (como o diagrama adaptado da ISO/IEC 25010) e tabelas (Linha do Tempo, GQM e Custos) sejam numeradas, possuam título/legenda, indiquem a fonte (ex.: *Fonte: Elaborado pelos autores*) e sejam explicitamente citadas no texto antes de aparecerem.
4. **Critério F3-C7 (GitPage da Equipe):** Garantir que a GitPage tenha menu claro, links funcionais para o repositório e para a * release*, seção explícita de última atualização e rastreabilidade completa das Fases 1, 2 e 3.