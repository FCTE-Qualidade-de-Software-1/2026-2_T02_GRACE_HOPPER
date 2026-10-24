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

Para garantir pontuação máxima na rubrica da Fase 1, os requisitos da avaliação estão estruturados nos seis subitens abaixo:

#### 2.1.1 Contextualização do Produto (i-Educar)

- Sistema de Gestão Escolar *open source* desenvolvido originalmente em PHP e modernizado com o *framework* Laravel, mantido pela comunidade e pela Portabilis.
- Gerencia matrículas, turmas, enturmações, diários de classe, lançamento de notas/frequências, emissão de históricos e exportação direta para o Censo Escolar (Educacenso/INEP).

#### 2.1.2 Propósito da Avaliação e Uso Pretendido

- **Propósito:** Avaliar a qualidade de produto (ISO/IEC 25010:2023) e, de forma complementar, a qualidade em uso (ISO/IEC 25019:2023) dos módulos de **Matrícula** e de **Lançamento de Notas e Menções** do i-Educar 2.12, verificando se esses módulos oferecem o nível de confiabilidade, manutenibilidade, compatibilidade e capacidade de interação exigido por redes públicas de ensino.
- **Natureza da avaliação:** avaliação independente e diagnóstica, conduzida por avaliadores externos ao projeto i-Educar. Não constitui certificação nem homologação oficial do software.
- **Uso pretendido dos resultados:** a Tabela 1 relaciona cada decisão que a avaliação pretende apoiar, quem a toma e qual resultado a informa.

**Tabela 1 — Decisões apoiadas pelos resultados da avaliação**

| Quem decide | Decisão apoiada | Resultado da avaliação que informa a decisão |
| :--- | :--- | :--- |
| Secretarias Municipais de Educação (gestores e equipes de TI) | Adotar, manter ou atualizar o i-Educar para matrícula e diário de classe; definir se a adoção exige suporte técnico contratado ou customizações. | Resultado dos critérios eliminatórios de confiabilidade (cálculo de notas e integridade das operações de matrícula) e índice de qualidade por característica. |
| Mantenedores (Portabilis e comunidade i-Educar) | Priorizar refatorações, testes e correções nos módulos avaliados. | Métricas de manutenibilidade e de proteção contra erros do usuário, com os pontos críticos localizados no código. |
| Integradores (equipes de TI municipais) | Integrar o i-Educar a outros sistemas municipais no mesmo ambiente e via API, sem adaptações extras. | Métricas de compatibilidade (coexistência de recursos e conformidade das respostas da API). |
| Secretários escolares e professores (representados pelas Secretarias) | Definir a necessidade de capacitação para matrícula e lançamento de notas. | Métricas de capacidade de interação e de qualidade em uso (tempo de tarefa e sucesso na primeira tentativa). |

*Fonte: Elaborado pelos autores.*

#### 2.1.3 Identificação do Requisitante e Partes Interessadas (Stakeholders)

As partes interessadas foram caracterizadas pelo papel que exercem no i-Educar, pela necessidade principal e pela característica do modelo de qualidade que as afeta. A Tabela 1-A consolida essa caracterização. Os perfis de secretários escolares e professores são os usuários finais primários; os integradores (equipes de TI municipais e o INEP) são os usuários secundários.

**Tabela 1-A — Caracterização das partes interessadas no i-Educar**

| Parte interessada | Perfil e papel no i-Educar | Necessidade principal | Característica avaliada (ISO/IEC 25010:2023) |
| :--- | :--- | :--- | :--- |
| **Secretários escolares** (usuários finais primários) | Registram matrículas e enturmações (`pmieducar.matricula` e `pmieducar.matricula_turma`). | Entrada de dados sem erro, com mensagens claras quando há bloqueio. | Capacidade de Interação (M12 a M15) |
| **Professores** (usuários finais primários) | Lançam notas e menções no diário (`modules.nota_componente_curricular`). | Cálculo de notas determinístico e diário sem perda de dados. | Confiabilidade (M3 e M4); Capacidade de Interação (M14 e M15) |
| **Gestores municipais** (Secretarias Municipais de Educação) | Decidem a adoção, a manutenção e a necessidade de suporte técnico do sistema (Tabela 1). | Dados confiáveis para decisão e prestação de contas. | Confiabilidade (Gates) e índice global IQM |
| **Equipes de TI municipais** (integradores de sistemas municipais) | Integram o i-Educar a outros sistemas municipais pela API REST (`routes/api.php` e `routes/api_v2.php`) e mantêm a convivência no mesmo ambiente. | Contratos de API estáveis e convivência sem conflito de recursos. | Compatibilidade (M1 e M2) |
| **Integradores do INEP** (sistemas de coleta do Censo Escolar) | Recebem os dados do Censo Escolar enviados pelas secretarias, gerados pelo módulo Educacenso (pacote `i-educar-educacenso-package`). | Dados do Censo fiéis aos registros de matrícula e de notas. | Fora do escopo direto da avaliação; a dependência desses dados é tratada como risco de Confiabilidade. |
| **Mantenedores** (Portabilis e comunidade i-Educar) | Mantêm o código dos módulos avaliados e recebem as correções que a avaliação identificar. | Código analisável, modificável e testável. | Manutenibilidade (M7 a M11) |

*Fonte: elaborado pelos autores a partir dos modelos e rotas do repositório `portabilis/i-educar` (branch `2.12`, commit `7903a3efc7689942ee700007f86ed581023aad27`) e do Framework GQM.*

#### 2.1.4 Seleção, Priorização e Adaptação do Modelo de Qualidade (ISO/IEC 25010:2023)

O modelo adaptado da ISO/IEC 25010 destaca as **4 características** e respectivas **subcaracterísticas** recortadas para o i-Educar. A Figura 1 do [framework GQM](gqm_evaluation_framework.md#figura-1-adaptacao-da-isoiec-250102023-ao-recorte-da-avaliacao) apresenta o diagrama próprio da equipe; não é reprodução da figura normativa. A página pública da ISO descreve nove características, mas a íntegra da edição é paga. Portanto, a figura identifica o recorte e seus termos como adaptação da equipe, não como transcrição integral verificada.

- **Capacidade de Interação** (característica obrigatória na disciplina / foco em interação): *Proteção contra erros do usuário* e *Autodescritividade* são operacionalizadas por M12 e M13. Apreensibilidade e operabilidade aparecem como necessidades de contexto, mas não têm métricas próprias nesta versão. Justificativa: perfil heterogêneo de letramento digital dos servidores escolares e necessidade de evitar erros de preenchimento cadastral.
- **Compatibilidade** (1ª característica adicional): *Coexistência* e *Interoperabilidade*. Justificativa: dependência obrigatória de troca de dados com o sistema Educacenso (INEP) e integração via API REST com sistemas municipais.
- **Confiabilidade** (2ª característica adicional): *Ausência de Falhas (Faultlessness, termo usado no framework)*, *Tolerância a falhas* e *Recuperabilidade*. “Maturidade” é nomenclatura anterior registrada em documentos do projeto, não uma equivalência normativa afirmada neste relatório. Justificativa: alta criticidade durante períodos de matrícula e fechamento de bimestres letivos; falhas nesses períodos podem comprometer registros e cálculos escolares.
- **Manutenibilidade** (3ª característica adicional): *Modularidade*, *Analisabilidade*, *Modificabilidade* e *Testabilidade*. Justificativa: coexistência de código legado (`ieducar/intranet`) com código moderno em Laravel (`app/`), exigindo facilidade de manutenção para adaptar regras de avaliação específicas de cada município.

**Método de priorização das características:** a Capacidade de Interação, conforme o recorte apresentado pela equipe e requisito da disciplina, é obrigatória e, por isso, não participa da priorização; entra na avaliação com peso fixo. As demais alternativas registradas pela equipe foram comparadas em uma matriz de criticidade com três critérios, pontuados de 1 (baixo) a 5 (alto):

- **Impacto ($I$):** gravidade da consequência para os *stakeholders* caso os módulos avaliados apresentem baixa qualidade na característica.
- **Risco ($R$):** probabilidade de haver problemas na característica, considerando a arquitetura do i-Educar (núcleo legado em `ieducar/` convivendo com código Laravel em `app/`) e seu tempo de uso em produção.
- **Viabilidade de medição ($V$):** possibilidade de coletar evidências objetivas com os recursos da equipe (ambiente Docker local, código-fonte aberto, sem acesso a ambientes de produção).

A criticidade é calculada como $C = I \times R$. São selecionadas as três características de maior criticidade que tenham $V \ge 3$; em caso de empate, prevalece a maior viabilidade. A Tabela 2 apresenta o resultado.

**Tabela 2 — Matriz de priorização das características da ISO/IEC 25010:2023**

| Característica | I | R | V | C = I × R | Decisão | Peso no índice global |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| Manutenibilidade | 4 | 5 | 5 | 20 | Selecionada | 30% |
| Confiabilidade | 5 | 4 | 4 | 20 | Selecionada | 30% |
| Segurança | 5 | 4 | 2 | 20 | Excluída (V < 3) | — |
| Compatibilidade | 4 | 3 | 3 | 12 | Selecionada | 20% |
| Adequação Funcional | 5 | 2 | 4 | 10 | Excluída (criticidade menor) | — |
| Eficiência de Desempenho | 3 | 3 | 2 | 9 | Excluída (V < 3) | — |
| Flexibilidade (antiga Portabilidade) | 2 | 2 | 4 | 4 | Excluída (criticidade menor) | — |
| Capacidade de Interação | — | — | — | — | Obrigatória (fora da priorização) | 20% |

*Fonte: Elaborado pelos autores.*

**Limite da matriz:** esta tabela registra as alternativas consideradas pela equipe e não enumera todas as nove características mencionadas no resumo público da ISO/IEC 25010:2023. A característica que não aparece na tabela não recebeu nome, pontuação ou decisão nesta revisão; completar essa lacuna exige consulta ao texto normativo e decisão da equipe. A ISO não prescreve os pesos de 30% / 30% / 20% / 20%, que são uma decisão local.

<div class="grid cards" markdown>

-   **Justificativa das Pontuações do Recorte**

    ---

    - **Manutenibilidade ($R = 5$):** a convivência entre o núcleo legado e o código Laravel aumenta o risco de baixa analisabilidade e testabilidade; a medição é altamente viável por análise estática do código aberto ($V = 5$).
    - **Confiabilidade ($I = 5$):** erros no cálculo de médias ou operações de matrícula incompletas afetam diretamente a vida escolar do estudante e os dados oficiais da rede.
    - **Compatibilidade ($I = 4, R = 3, V = 3$):** o i-Educar compartilha banco de dados, cache e portas com outros serviços municipais e expõe uma API REST para integrações; a medição é viável, porém depende de montar um segundo serviço no ambiente local.
    - **Adequação Funcional ($R = 2$):** as funções de matrícula e notas estão em uso em produção em diversos municípios há anos, o que torna improvável a ausência de funções essenciais; além disso, a exatidão do cálculo de notas já é verificada pela métrica de ausência de falhas em Confiabilidade.

-   **Trade-offs da Priorização**

    ---

    - **Exclusão de Segurança:** escolha mais sensível, pois o i-Educar armazena dados pessoais de estudantes, em grande parte menores de idade, protegidos pela LGPD. Uma avaliação com evidência objetiva exigiria testes de intrusão e varredura de vulnerabilidades, com riscos éticos e de infraestrutura incompatíveis com o prazo da disciplina; uma avaliação superficial produziria conclusões frágeis. A equipe registra essa lacuna como limitação do estudo.
    - **Equilíbrio de Pesos (30% / 30%):** atribuir o mesmo peso (30%) a Manutenibilidade e Confiabilidade privilegia a visão de mantenedores e gestores sobre a do usuário final; esse desequilíbrio é compensado pela inclusão obrigatória da Capacidade de Interação com métricas de qualidade em uso.
    - **Escopo de Compatibilidade (20%):** restrito à coexistência no ambiente e à API REST do núcleo; a exportação para o Educacenso/INEP fica fora do escopo por ser distribuída em pacote separado (`i-educar-educacenso-package`).

</div>

#### 2.1.5 Escopo, Profundidade e Objetos de Avaliação

O foco em **Matrícula** e **Notas/Menções** decorre da criticidade dos registros para secretarias, professores e gestores (Tabelas 1 e 1-A) e da arquitetura observada nos artefatos do produto: vínculo e enturmação em `pmieducar.matricula`/`matricula_turma` e seus modelos/serviço Laravel; regras pedagógicas, diário e cálculos em `modules` e no subsistema legado `ieducar/modules/Avaliacao`. A avaliação é diagnóstica desses fluxos, não certificação do produto completo.

<div class="grid cards" markdown>

-   **Dentro do Escopo (Objetos Avaliados)**

    ---

    - Fluxos e código de matrícula, enturmação, remanejamento, ciclo de vida do vínculo escolar, diário, regras de avaliação, notas e menções (Interação/Uso, Confiabilidade e Manutenibilidade).
    - *Endpoints* da API REST do núcleo e isolamento de recursos de ambiente via Docker (Compatibilidade).
    - Determinismo de cálculo, operações transacionais e planejamento/teste de restauração dos esquemas `pmieducar`, `modules` e `cadastro` em ambiente local ou de homologação (Confiabilidade).
    - Análise estática dos caminhos de código associados nos diretórios `app/` e `ieducar/` (Manutenibilidade); M5 é definido, mas depende de registros de produção para ser mensurado.

-   **Fora do Escopo (Exclusões Justificadas)**

    ---

    - Teste sob estresse simultâneo de múltiplos municípios; não há infraestrutura representativa da produção disponível para esta avaliação.
    - Pacotes de terceiros e bibliotecas externas na pasta `vendor/` ou repositórios separados como `i-educar-educacenso-package` (avalia-se apenas o código sob responsabilidade direta do núcleo do i-Educar).
    - Segurança como característica avaliada, eficiência de desempenho em escala, integrações que dependam de credenciais/dados de produção e módulos que não sejam Matrícula e Notas/Menções.

</div>

#### 2.1.6 Relação com os Objetivos de Desenvolvimento Sustentável (ODS da ONU)

A Tabela 1-B apresenta os textos oficiais das metas publicados pela ONU, os indicadores oficiais de acompanhamento e a justificativa do vínculo com o i-Educar. O vínculo é indireto: a avaliação mede a qualidade do produto, e não os resultados educacionais ou institucionais que as metas acompanham.

**Tabela 1-B — Metas dos ODS 4 e 16 relacionadas ao i-Educar**

| ODS e meta | Texto oficial da meta (ONU) | Indicadores oficiais de acompanhamento | Justificativa do vínculo com o i-Educar |
| :--- | :--- | :--- | :--- |
| **ODS 4, Meta 4.1** | "By 2030, ensure that all girls and boys complete free, equitable and quality primary and secondary education leading to relevant and effective learning outcomes" (tradução livre: até 2030, garantir que todas as meninas e todos os meninos concluam o ensino primário e secundário gratuito, equitativo e de qualidade, com resultados de aprendizagem relevantes e eficazes). | 4.1.2: taxa de conclusão (primário, fundamental e médio). | O i-Educar registra matrículas, enturmações e notas, que alimentam a gestão escolar e os dados do Censo Escolar. Não se mede conclusão nem evasão nesta avaliação. |
| **ODS 4, Meta 4.a** | "Build and upgrade education facilities that are child, disability and gender sensitive and provide safe, non-violent, inclusive and effective learning environments for all" (tradução livre: construir e adaptar instalações educacionais sensíveis a crianças, pessoas com deficiência e gênero, com ambientes de aprendizagem seguros, não violentos, inclusivos e eficazes para todos). | 4.a.1: proporção de escolas com serviços básicos, por tipo de serviço. | O vínculo é limitado: o sistema não atua sobre a infraestrutura física das escolas. Ele contribui apenas pela gestão dos registros escolares. |
| **ODS 16, Meta 16.6** | "Develop effective, accountable and transparent institutions at all levels" (tradução livre: desenvolver instituições eficazes, responsáveis e transparentes em todos os níveis). | 16.6.1: despesas primárias do governo como proporção do orçamento aprovado; 16.6.2: proporção da população satisfeita com a última experiência em serviços públicos. | Registros escolares rastreáveis, cálculo de notas verificável e código aberto e auditável favorecem a transparência administrativa. Essa relação é qualitativa e não é medida pela avaliação. |

*Fonte: textos das metas e indicadores extraídos de <https://sdgs.un.org/goals/goal4> e <https://sdgs.un.org/goals/goal16>; justificativas elaboradas pelos autores.*

**Justificativa do i-Educar como Bem Público Digital aberto.** A equipe classifica o i-Educar como Bem Público Digital. Essa afirmação se apoia em três fatos verificados: o software é licenciado sob GPL-2.0-or-later (`composer.json`), é de acesso público e gratuito e é mantido pela Portabilis, conforme publicação do BID. O registro formal como Bem Público Digital não foi verificado nas fontes consultadas, e a classificação deve ser tratada como afirmação da equipe.

---

### 2.2. Fase 2: Especificar a Avaliação (GQM e Critérios de Julgamento)

Nesta fase, a equipe transforma as 4 características em medições concretas utilizando a abordagem **GQM (Goal-Question-Metric)** e estabelece as regras matemáticas de aprovação.

#### Quadro Resumo do GQM Proposto para o i-Educar

| Característica (Subcaracterística) | Objetivo (Goal - GQM) | Questões (Questions) | Métricas e Fórmulas (Metrics) | Níveis de Pontuação e Critério de Julgamento |
| :--- | :--- | :--- | :--- | :--- |
| **Compatibilidade** (*Coexistência e Interoperabilidade*) | Analisar o ambiente de execução e a API REST do i-Educar com o propósito de avaliar a coexistência e a interoperabilidade sob o ponto de vista de integradores técnicos. | **Q1.1:** Os recursos de ambiente podem ser isolados por configuração sem conflito?<br>**Q1.2:** As respostas da API obedecem a um contrato de dados verificável? | **M1 ($\text{TINCR}$):**<br>$\text{TINCR} = \dfrac{N_{\text{isoláveis}}}{N_{\text{identificados}}} \times 100\%$<br><br>**M2 ($\text{CEI}$):**<br>$\text{CEI} = \dfrac{N_{\text{endpoints conformes}}}{N_{\text{endpoints testados}}} \times 100\%$ | **Crítico (1):** $< 70\%$<br>**Regular (2):** $[70\%, 85\%)$<br>**Bom (3):** $[85\%, 100\%)$<br>**Excelente (4):** $100\%$ |
| **Confiabilidade** (*Ausência de Falhas, Tolerância a Falhas e Recuperabilidade*) | Analisar os fluxos críticos de notas e matrícula com o propósito de avaliar o determinismo de cálculo e a integridade transacional sob o ponto de vista da gestão escolar. | **Q2.1:** O cálculo de notas e menções é 100% determinístico?<br>**Q2.2:** Operações compostas garantem rollback integral sem dados órfãos? | **M3 ($\text{DCNM}$ — Gate):**<br>$\text{DCNM} = \dfrac{N_{\text{casos conformes}}}{N_{\text{casos planejados no manifesto}}} \times 100\%$<br><br>**M4 ($\text{ITAE}$ — Gate):**<br>$\text{ITAE} = \dfrac{N_{\text{operações com todos os rollbacks verificados}}}{N_{\text{operações compostas planejadas}}} \times 100\%$ | **Gates Binários (M3 e M4):**<br>**Reprovado:** $< 100\%$<br>**Aprovado:** $100\%$ |
| **Manutenibilidade** (*Modularidade, Analisabilidade, Modificabilidade e Testabilidade*) | Analisar o código-fonte do repositório `portabilis/i-educar` com o propósito de avaliar a facilidade de manutenção e testabilidade sob o ponto de vista dos mantenedores. | **Q3.1:** Qual a complexidade ciclomática dos métodos no universo declarado?<br>**Q3.4 / Q3.5:** Qual o índice de manutenibilidade e a taxa de testes ativos com asserção? | **M7a/M7b ($\text{CC}$):** $v(G) = E - N + 2P$; P90 e máximo.<br><br>**M10 ($\text{MI}$):** escala local normalizada $[0, 100]$<br><br>**M11 ($\text{TTAE}$):**<br>$\text{TTAE} = \dfrac{N_{\text{testes ativos com asserção}}}{N_{\text{casos declarados no manifesto}}} \times 100\%$ | **M7a ($\text{CC}_{P90}$):** Excelente $\le 10$; Crítico $> 20$.<br>**M7b ($\text{CC}_{\max}$):** conforme tabela do framework.<br>**M10 ($\text{MI}$):** Excelente $\ge 80$; Crítico $< 40$.<br>**M11 ($\text{TTAE}$):** Excelente $\ge 95\%$; Crítico $< 70\%$. A asserção não prova eficácia; eficácia exige teste controlado separado. |
| **Capacidade de Interação e Qualidade em Uso** (*Proteção contra erros, Autodescritividade, Eficiência e Eficácia*) | Analisar os fluxos de matrícula e diário de classe com o propósito de avaliar a prevenção de erros e a eficiência/eficácia operacional sob o ponto de vista de secretários e professores. | **Q4.1 / Q4.2:** O sistema bloqueia entradas inválidas com mensagens claras?<br>**Q4.3 / Q4.4:** Qual a razão de tempo e o sucesso na 1ª tentativa em uso? | **M12 ($\text{IPPE}$ — Gate):**<br>$\text{IPPE} = \dfrac{N_{\text{bloqueios amigáveis}}}{N_{\text{cenários inválidos}}} \times 100\%$<br><br>**M14 ($R_{\text{tempo},T}$):** $R_{\text{tempo},T} = \dfrac{\text{TMET}_T}{T_{\text{ref},T}}$<br><br>**M15 ($\text{TSPT}$):** $\text{TSPT} = \dfrac{N_{\text{1ª submissão}}}{N_{\text{execuções}}} \times 100\%$ | **M12 (Gate):** $100\%$<br>**M14 ($R_{\text{tempo}}$):** Excelente $\le 1{,}5$; Crítico $> 3{,}0$.<br>**M15 ($\text{TSPT}$):** Excelente $\ge 90\%$; Crítico $< 50\%$. |

Para M3 e M4, os denominadores são manifestos planejados e congelados antes da execução. Universo vazio, cobertura incompleta ou evidência ausente não aprova o gate (não se interpreta `0/0` como 100%); os procedimentos completos estão no framework GQM.

---

### 2.3. Fase 3: Projetar a Avaliação (Plano de Avaliação e Ferramentas)

Para demonstrar planejamento completo e alinhamento com a futura execução (Fase 4), o projeto da avaliação estrutura o ambiente e os instrumentos de coleta em três frentes operacionais:

#### 2.3.1 Ambiente Conteinerizado de Testes e Reprodutibilidade (Docker Compose — Issue #10)

Para assegurar a reprodutibilidade científica da avaliação independente, o ambiente de testes utiliza uma infraestrutura conteinerizada padronizada via Docker Compose, ancorada nas seguintes definições de versionamento:

* **Repositório Base:** `https://github.com/portabilis/i-educar` (branch oficial `2.12`, commit congelado de referência `7903a3efc7689942ee700007f86ed581023aad27`).
* **Serviço de Aplicação (`app`):** Imagem conteinerizada `portabilis/i-educar:2.12.0` executando PHP 8.5 e framework Laravel 13, exposta localmente na porta `8080`.
* **Serviço de Banco de Dados (`database`):** PostgreSQL versão 18 (`postgres:18-alpine`) com esquemas relacionais `pmieducar`, `modules` e `cadastro`, exposto na porta `5432`.
* **Serviço de Cache e Sessão (`cache`):** Redis 7 (`redis:7-alpine`) operando na porta `6379`.

**Procedimento Sequencial de Inicialização e Carga Pedagógica:**

1. Validação do arquivo de composição conteinerizada:
   ```bash
   docker compose config
   ```
2. Inicialização dos serviços em segundo plano:
   ```bash
   docker compose up -d
   ```
3. Execução das migrações de banco e carga de sementes de teste (*seeders* controlados com regras de avaliação pré-configuradas):
   ```bash
   docker compose exec app php artisan migrate --seed
   ```
4. Verificação de prontidão dos endpoints de API via healthcheck HTTP (status code 200).

---

#### 2.3.2 Métodos e Ferramentas de Análise Estática (SonarQube e Motor PHP CLI — Issue #11)

A medição das métricas da característica **Manutenibilidade** (M7a, M7b, M8, M9, M10 e M11) articula ferramentas consagradas de mercado com scripts de automação proprietários:

* **SonarQube / PHPMetrics:** Utilizados para cálculo global de cobertura de código, métricas estruturais de acoplamento e complexidade ciclomática.
* **Motor Proprietário de Inspeção (`scripts/evaluate-quality.php`):** Script executável desenvolvido em PHP CLI nativo, capaz de percorrer a árvore de arquivos de `app/` e `ieducar/modules/`, aplicando análise léxica (*token_get_all*) para:
    * Calcular o $P_{90}$ e o valor máximo da Complexidade Ciclomática ($\text{CC}_{P90}$ e $\text{CC}_{\max}$ — M7a e M7b).
    * Computar a Distância da Sequência Principal de Martin ($\text{DSPM}$ — M8) e o Índice de Fricção de Dados Legado-Moderno ($\text{IFDL}$ — M9).
    * Gerar o Índice de Manutenibilidade Normalizado ($\text{MI}$ — M10).
    * Auditar a suíte de testes com detecção automatizada de asserções ativas e contagem de testes pulados com `markTestSkipped()` ($\text{TTAE}$ — M11).
* **Formatos de Saída:** Suporte nativo a relatório tabular em console e saída em JSON estruturado para consumo em pipelines de integração contínua:
   ```bash
   php scripts/evaluate-quality.php --format=table
   php scripts/evaluate-quality.php --format=json
   ```

---

#### 2.3.3 Protocolo Experimental de Usabilidade e Conformidade Ética (TCLE — Issue #12)

Para a medição empírica das métricas de **Capacidade de Interação** e **Qualidade em Uso** (M12, M13, M14a, M14b e M15), foi formulado um protocolo experimental estruturado em tarefas guiadas com secretários escolares e professores:

* **Tarefa 1 (T1 — Matrícula e Enturmação):** Cadastro de novo estudante e enturmação em turma de 6º ano, com registro de tempo de conclusão ($R_{\text{tempo},T1}$ — M14a) e taxa de submissão na 1ª tentativa ($TSPT$ — M15).
* **Tarefa 2 (T2 — Diário de Classe e Notas):** Lançamento de notas e menções bimestrais no diário eletrônico com cálculo automático de média ponderada ($R_{\text{tempo},T2}$ — M14b).
* **Salvaguardas Éticas e Documento Formal:** Em observância à Resolução CNS nº 510/2016 e à LGPD (Lei nº 13.709/2018), a coleta assegura total anonimização dos participantes, voluntariedade de participação e uso restrito a ambiente de homologação. O documento completo encontra-se publicado na GitPage em:
  [Termo de Consentimento Livre e Esclarecido (TCLE)](termo_consentimento_livre_esclarecido.md).

---

## 3. Gestão de Recursos, Esforço e Custos (PSM/CID e Critério AG-C5)

Conforme solicitado pela professora e exigido pela métrica de **Recursos e Custos (PSM/CID)** e pelo critério **AG-C5 (Transparência da Contribuição Individual)**, a tabela abaixo unifica as tarefas executadas, a quantidade de horas dedicadas, o **valor por hora de cada integrante** e o **percentual de esforço (somando 100%)**.

| Integrante | Papel Principal na Equipe | Responsabilidades e Tarefas no Ponto de Controle 1 | Horas Dedicadas (h) | Valor / Hora (R$) | Custo Total (R$) | % de Esforço (AG-C5) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Arthur Soares Parente** | Gestor de Configuração / GitPage | Configuração do repositório, templates de issue e estrutura da GitPage (Issue #01). | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Fábio Santos Araujo** | Redação do Artigo | Primeira versão do artigo no Overleaf (Issue #13). | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gabriel Barbaceli** | GitPage / Especificação GQM | Propósito, uso pretendido e priorização (Issue #17); especificação GQM de **Compatibilidade** e de **Capacidade de Interação** (Issues #05 e #08); tabela de integrantes (Issue #19). | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Gustavo Silva Rodrigues** | Analista de Qualidade / Modelagem | Modelo ISO/IEC 25010 adaptado e delimitação de escopo (Issue #04). | 12h | R$ 50,00 | R$ 600,00 | **16,67%** |
| **Ítalo Alves Sampaio de Oliveira** | Analista do Produto e Stakeholders / GitPage | Contextualização do i-Educar (Issue #02); stakeholders e ODS 4 e 16 (Issue #03). | 12h | R$ 50,00 | R$ 600,00 | **16,66%** |
| **Ricardo Lucas Winchello Vieira Branco** | Redação do Artigo | Primeira versão do artigo no Overleaf (Issue #13). | 12h | R$ 50,00 | R$ 600,00 | **16,66%** |
| **TOTAL DA EQUIPE** | — | **Entregáveis Consolidados até o Ponto de Controle 1** | **72h** | Média: R$ 50,00/h | **R$ 3.600,00** | **100%** |

---

## 4. Estrutura da Apresentação de Slides para o Ponto de Controle 1

Como o objetivo da apresentação é mostrar o andamento do projeto, a linha do tempo, o ponto atual e os próximos passos (em vez de ler trechos longos do artigo), recomenda-se uma apresentação objetiva de **8 slides**:

| Slide | Tópico Principal | Conteúdo e Evidências Apresentadas |
| :---: | :--- | :--- |
| **Slide 1** | **Capa e Identificação** | Título do projeto (*Avaliação de Qualidade do Sistema de Gestão Escolar i-Educar sob a Ótica da Família ISO/IEC 25000 — SQuaRE*), integrantes, link do repositório avaliado (`portabilis/i-educar`) e link da GitPage. |
| **Slide 2** | **Linha do Tempo ("Onde Estamos")** | Exibição visual da **Tabela da Seção 1** destacando o marco concluído (**M0**), o estágio atual (**M1/M2 — Ponto de Controle 1**) e os próximos passos até a **Release E1** e **Entrega 2**. |
| **Slide 3** | **Fase 1: Objeto, Propósito e Stakeholders** | Visão da arquitetura do **i-Educar** (PHP/Laravel), propósito da avaliação, partes interessadas (Secretarias Municipais, Portabilis, Professores/Secretários) e alinhamento com os **ODS 4 e ODS 16 da ONU**. |
| **Slide 4** | **Fase 1: Modelo Adaptado (ISO/IEC 25010) e Escopo** | Apresentação do recorte das 4 características (**Compatibilidade, Confiabilidade, Manutenibilidade e Capacidade de Interação**), matriz de priorização ($C = I \times R$) e quadro "Dentro vs. Fora do Escopo". |
| **Slide 5** | **Fase 2: Especificação GQM (Compatibilidade e Confiabilidade)** | Síntese visual dos Objetivos, Questões, Métricas (`M1` a `M6`) e Gates Binários (`M3` e `M4`) para a API/ambiente (Compatibilidade) e determinismo/transações (Confiabilidade). |
| **Slide 6** | **Fase 2: Especificação GQM (Manutenibilidade e Interação/Uso)** | Síntese visual dos Objetivos, Questões, Métricas (`M7` a `M15`) e Critérios de Julgamento para o código-fonte (Manutenibilidade) e fluxos de matrícula/diário (Capacidade de Interação e Qualidade em Uso). |
| **Slide 7** | **Gestão do Projeto (PSM/CID)** | Apresentação da **Tabela da Seção 3** com o papel de cada integrante, horas dedicadas (`72h`), valor/hora (`R$ 50,00/h`), custo total acumulado (`R$ 3.600,00`) e percentual de esforço somando **100%**. |
| **Slide 8** | **Próximos Passos e Entregáveis** | Validação do GQM no Ponto de Controle 1, consolidação do Plano de Avaliação (Fase 3: Docker, SonarQube, Postman, TCLE), fechamento da 1ª versão do Artigo, revisão da GitPage (**F3-C7**) e publicação da *Release E1*. |

---

## 5. Checklist de Qualidade Documental (Prevenção de Penalidades na Rubrica)

Antes de apresentar e gerar a *Release*, a equipe valida os seguintes critérios obrigatórios das diretrizes da disciplina:

<div class="grid cards" markdown>

-   **1. Critério AG-C3 — Zero Emojis / Figurinhas**

    ---

    Verificar que a GitPage e o Artigo não possuem nenhum emoji, ícone decorativo ou figurinha no corpo do texto e nos títulos.

-   **2. Critério AG-C3 — Declaração de Uso de IA**

    ---

    Manter seção explícita no artigo e na GitPage informando qual ferramenta de IA foi utilizada, para quais tarefas de apoio e como a equipe revisou e validou tecnicamente todo o conteúdo.

-   **3. Critérios AG-C2 e AG-C4 — Rigor Editorial**

    ---

    Garantir que todas as figuras e tabelas (Linha do Tempo, Priorização, GQM e Custos) sejam numeradas, possuam título/legenda, indiquem a fonte (*Fonte: Elaborado pelos autores*) e sejam citadas no texto.

-   **4. Critério F3-C7 — GitPage da Equipe**

    ---

    Garantir que a GitPage tenha menu claro, links funcionais para o repositório e para a *release*, identificação de última atualização no rodapé e rastreabilidade completa das Fases 1, 2 e 3.

</div>
