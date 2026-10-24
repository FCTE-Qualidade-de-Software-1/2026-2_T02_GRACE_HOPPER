# Esqueleto do artigo — validação com a GitPage

Roteiro de conferência da Entrega 1, na ordem do artigo atual. As caixas começam desmarcadas: representam itens a validar pelo grupo, não uma certificação de conformidade.

**Base documental:** commit `8941b9c`, com as revisões locais do artigo. **Contagem:** 4 objetivos, 14 questões, 15 medições (famílias M1–M15) e 17 linhas operacionais.

**Como usar:** abrir o [PDF](main.pdf), comparar cada bloco com a fonte indicada e marcar `[x]` após a conferência. Registrar dúvidas no campo “Observações” do bloco. Os links locais apontam para os documentos que alimentam a GitPage; a versão publicada pode estar em outra revisão.

## Fontes para comparação

| Documento | Arquivo local | GitPage |
| --- | --- | --- |
| Planejamento PC1 | [Planejamento](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md) | [Abrir página](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/relatorio_de_planejamento_ponto_de_controle_1_i_educar/) |
| Framework GQM | [GQM](../gqm_evaluation_framework.md) | [Abrir página](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/gqm_evaluation_framework/) |
| Gestão e contribuições | [Gestão](../gestao_projeto_releases_milestones_issues.md) | [Abrir página](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/gestao_projeto_releases_milestones_issues/) |
| Arquitetura | [Arquitetura](../agents/architecture.md) | [Abrir página](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/agents/architecture/) |
| Contexto do produto | [Visão do produto](../agents/project_overview.md) | [Abrir página](https://fcte-qualidade-de-software-1.github.io/2026-2_T02_GRACE_HOPPER/agents/project_overview/) |

## Elementos iniciais

- [ ] **Título:** Avaliação da Qualidade do i-Educar com Base na ISO/IEC 25010:2023 e ISO/IEC 25019:2023: Estudo de Caso nos Módulos de Matrícula e Lançamento de Notas.
- [ ] **Autores:** seis integrantes; nomes, matrículas, afiliação e e-mails.
- [ ] **Resumo:** objeto, escopo, normas, Fases 1 e 2, contagem GQM e execução prevista para a Entrega 2.
- [ ] **Palavras-chave:** coerentes com o tema e os métodos.

**Comparar com:** visão do produto; planejamento §2; gestão §1.

**Observações:** ______

## I. Introdução

- [ ] Contexto da gestão escolar e riscos de inconsistências em matrículas e notas.
- [ ] Justificativa da escolha do i-Educar.
- [ ] Recorte: Matrícula de Alunos e Lançamento de Notas e Menções.
- [ ] Quatro características do produto; eficácia e eficiência em uso como complemento.
- [ ] Objetivo geral, objetivos específicos e contribuição da Entrega 1.
- [ ] Organização do artigo, repositório, GitPage e identificação da release E1.

**Comparar com:** visão do produto; planejamento §§2.1.1–2.1.2; gestão §4.

**Observações:** ______

## II. Referencial Teórico

### A. Qualidade de produto, qualidade em uso e a família SQuaRE

- [ ] Papel de cada norma: ISO/IEC 25010:2023, 25019:2023, 25023:2016, 25040:2024 e 25002:2024.
- [ ] Separação entre modelo de produto, qualidade em uso e processo de avaliação.

### B. Características avaliadas

- [ ] Compatibilidade, Confiabilidade, Manutenibilidade e Capacidade de interação.
- [ ] Terminologia das edições adotadas e traduções utilizadas pela equipe.
- [ ] Distinção entre características completas e subcaracterísticas efetivamente avaliadas.

### C. Goal-Question-Metric (GQM) e PSM/CID

- [ ] Três níveis do GQM: conceitual, operacional e quantitativo.
- [ ] Template dos objetivos: objeto, propósito, foco, ponto de vista e contexto.
- [ ] Hipóteses como complemento adotado pelo estudo.
- [ ] PSM/CID aplicado ao acompanhamento da equipe.

**Comparar com:** GQM, abertura e §§1–3; planejamento §2.1.4; gestão §§1–2. A conferência das normas e da literatura exige também as fontes originais: concordância entre artigo e GitPage, isoladamente, não verifica a atribuição externa.

**Observações:** ______

## III. Metodologia

### A. Abordagem de avaliação e estratégia de medição

- [ ] Estudo de caso aplicado, diagnóstico e de abordagem mista.
- [ ] i-Educar: branch `2.12`, versão declarada `2.12.0`, commit `7903a3efc7689942ee700007f86ed581023aad27`.
- [ ] Ambiente Docker local e instrumentos previstos.
- [ ] Distinção entre especificar uma medição e apresentar um resultado coletado.

### B. Processo de avaliação

- [ ] Correspondência entre fases da disciplina e atividades do processo de avaliação.
- [ ] Fases 1 e 2 como conteúdo desta entrega; execução reservada à Entrega 2.

### C. Gestão do projeto com PSM/CID

- [ ] TCM: conclusão de issues planejadas.
- [ ] TRCD: conformidade documental dos PRs integrados.
- [ ] VEC: variação do esforço realizado em relação ao planejado.
- [ ] Evidências exigidas para calcular as taxas; planejamento não tratado como execução comprovada.
- [ ] **Tabela I:** plano de acompanhamento PSM/CID.

### D. Rastreabilidade, aspectos éticos e limitações

- [ ] Versionamento de produto, instrumentos, cenários e evidências.
- [ ] Dados fictícios, anonimização e TCLE previsto para participantes.
- [ ] Limitações de ambiente, amostra e generalização.
- [ ] M5 indisponível sem registros de produção; ausência de dados não equivale a zero.

**Comparar com:** arquitetura §§2 e 7; planejamento §§2–3; gestão §§1–2; GQM §§3 e 6.

**Observações:** ______

## IV. Fase 1: Definição da Avaliação

### A. Propósito da avaliação e uso pretendido

- [ ] Diagnóstico dos dois módulos e decisões que a avaliação pretende apoiar.

### B. Requisitante e partes interessadas

- [ ] Papéis da docente, equipe avaliadora, gestores, usuários, TI, mantenedores e sistemas externos.
- [ ] **Tabela II:** necessidades, critérios de sucesso, decisões e influência dos stakeholders.

### C. Tipo de produto e descrição estruturada

- [ ] Monólito híbrido: Laravel, legado PHP, PostgreSQL e componentes de apoio.
- [ ] Papel do `LegacyController` e limites das integrações externas.
- [ ] Viabilidade de coleta local versus medições dependentes de recursos adicionais.
- [ ] **Figura 1:** arquitetura e contexto; componentes externos tracejados.
- [ ] **Tabela III:** módulos, interfaces, tabelas e métricas associadas.

### D. Modelo de qualidade

- [ ] Quatro características escolhidas, subcaracterísticas mantidas e exclusões justificadas.
- [ ] **Figura 2:** modelo adaptado e relação com G1–G4.

### E. Seleção e priorização de características

- [ ] Impacto, risco e viabilidade; criticidade `C = I × R`; requisito `V ≥ 3`.
- [ ] Pesos: Compatibilidade 20%; Confiabilidade 30%; Manutenibilidade 30%; Interação/Uso 20%.
- [ ] **Tabela IV:** matriz, desempate, escolhas, exclusões e justificativas.

### F. Escopo, profundidade e objetos de avaliação

- [ ] Dois módulos; abordagens de caixa-branca, caixa-cinza e caixa-preta/uso.
- [ ] **Tabela V:** objetos incluídos, exclusões e motivos dos cortes.

### G. ODS, metas e indicadores relacionados

- [ ] Relação indireta com ODS 4 e 16; metas 4.1, 4.a e 16.6.
- [ ] **Tabela VI:** metas e indicadores oficiais, com ligação aos objetivos GQM.
- [ ] Relações propostas não apresentadas como impacto educacional já demonstrado.

**Comparar com:** planejamento §§2.1.1–2.1.6; arquitetura §§3–7; GQM §1.

**Observações:** ______

## V. Fase 2: Planejamento da Medição (GQM)

### A. Objetivos de medição e consistência entre as Fases 1 e 2

- [ ] G1: Compatibilidade — 2 questões.
- [ ] G2: Confiabilidade — 3 questões.
- [ ] G3: Manutenibilidade — 5 questões.
- [ ] G4: Capacidade de interação e qualidade em uso — 4 questões.
- [ ] **Tabela IX:** objetivos no template de cinco elementos e rastreabilidade com a Fase 1.

### B. Questões e hipóteses operacionais

Conferir a redação completa de cada questão e hipótese nas Tabelas VII e VIII. O quadro abaixo contém somente o tema e o vínculo com as métricas.

| Validado | Objetivo | Questão / hipótese | Tema | Linha(s) operacional(is) |
| --- | --- | --- | --- | --- |
| [ ] | G1 | Q1.1 / H1.1 | Coexistência e isolamento de recursos | M1 — TINCR |
| [ ] | G1 | Q1.2 / H1.2 | Contratos da API REST | M2 — CEI |
| [ ] | G2 | Q2.1 / H2.1 | Cálculo de notas e menções | M3 — DCNM, gate |
| [ ] | G2 | Q2.2 / H2.2 | Transações e defeitos operacionais | M4 — ITAE, gate; M5 — DDOM |
| [ ] | G2 | Q2.3 / H2.3 | Restauração de backups | M6 — CVPB |
| [ ] | G3 | Q3.1 / H3.1 | Complexidade ciclomática | M7a — CC-P90; M7b — CC-MAX |
| [ ] | G3 | Q3.2 / H3.2 | Distância da sequência principal | M8 — DSPM |
| [ ] | G3 | Q3.3 / H3.3 | Adaptações entre legado e moderno | M9 — IFDL |
| [ ] | G3 | Q3.4 / H3.4 | Índice de manutenibilidade | M10 — MI |
| [ ] | G3 | Q3.5 / H3.5 | Testes ativos com asserção | M11 — TTAE |
| [ ] | G4 | Q4.1 / H4.1 | Proteção contra erros | M12 — IPPE, gate |
| [ ] | G4 | Q4.2 / H4.2 | Clareza das mensagens | M13 — ADMV |
| [ ] | G4 | Q4.3 / H4.3 | Tempo relativo nas tarefas T1 e T2 | M14a — T1; M14b — T2 |
| [ ] | G4 | Q4.4 / H4.4 | Sucesso na primeira tentativa | M15 — TSPT |

### C. Métricas e fórmulas matemáticas de cálculo

#### 1. Compatibilidade (G1)

- [ ] M1 e M2: definição, fórmula, população, unidade, instrumento, evidência e critério.

#### 2. Confiabilidade (G2)

- [ ] M3–M6: definição, fórmula, população, unidade, instrumento, evidência e critério.
- [ ] M3/M4: manifestos prévios não vazios e tratamento de casos sem execução ou evidência.
- [ ] M5: janela de 90 dias; incidentes por mil movimentações; não mensurabilidade atual.

#### 3. Manutenibilidade (G3)

- [ ] M7a/M7b: mesmo universo de métodos; P90 por nearest rank e máximo.
- [ ] M8: componentes, dependências, abstratividade e convenções para denominadores nulos.
- [ ] M9: pontos lógicos de adaptação por modelo do manifesto.
- [ ] M10: variante local do MI, entradas válidas e média por método.
- [ ] M11: casos executados com asserção em tempo de execução.

#### 4. Capacidade de interação e Qualidade em uso (G4)

- [ ] M12/M13: cenários inválidos e classificação das mensagens.
- [ ] M14a/M14b: minutos coletados e razão adimensional usada no julgamento.
- [ ] T1: matrícula e enturmação de aluno já cadastrado; T2: notas de um componente para dez alunos.
- [ ] Pelo menos cinco iniciantes recrutados; número de concluintes por tarefa e referência de três execuções.
- [ ] M15: primeira submissão correta sobre o total de execuções.

### D. Níveis de pontuação, critérios de julgamento e gráfico GQM

- [ ] **Tabela VII:** G1 e G2; definições, hipóteses, limiares e pesos locais.
- [ ] **Tabela VIII:** G3 e G4; definições, hipóteses, limiares e pesos locais.
- [ ] **Figura 3:** quatro objetivos, 14 questões e 17 linhas; três níveis formais identificados.
- [ ] Gates M3, M4 e M12 exigem 100%; evidência insuficiente não produz aprovação.
- [ ] Níveis 4/3/2/1; agregação das métricas graduais em IQC e IQM.
- [ ] Métrica gradual sem resultado deixa os índices correspondentes não calculáveis, sem política prévia de exclusão.
- [ ] Critérios das classes A/B/C transcritos sem redefinição silenciosa.

**Comparar com:** GQM §§2–5; planejamento §2.2.

**Observações:** ______

## Declaração de Uso de Inteligência Artificial

- [ ] **Tabela X:** ferramentas, tarefas, período, verificações e limites.
- [ ] Distinguir revisão assistida de validação humana efetivamente realizada.
- [ ] Tabela X posicionada antes do início das referências.

**Comparar com:** declaração no README e registro efetivo de trabalho do grupo.

**Observações:** ______

## Referências

- [ ] Quinze entradas, citadas no texto e numeradas pela primeira ocorrência.
- [ ] Separar confirmação de metadados, leitura integral e suporte à afirmação citada.
- [ ] Título da ISO/IEC 25002:2024 corrigido com autorização: “Quality model overview and usage”.
- [ ] Consultas adicionais ao Article Galaxy e inclusão/substituição de fontes dependem de autorização do usuário.

**Comparar com:** bibliografia do artigo e fontes originais. A GitPage é fonte dos critérios locais, não substitui a conferência da literatura externa.

**Observações:** ______

## Apêndice A. Tabela de Contribuição dos Integrantes

- [ ] **Tabela XI:** seis integrantes; nomes, matrículas e responsabilidades.
- [ ] Planejamento: 12h e R$ 600 por integrante; totais de 72h e R$ 3.600.
- [ ] Percentuais arredondados somam 100%.
- [ ] Esforço planejado distinguido de horas efetivamente apontadas.

**Comparar com:** gestão §1; planejamento §3; README.

**Observações:** ______

## Pendências conhecidas para decisão do grupo

- [ ] README e abertura do GQM ainda informam 13 questões; a árvore contém 14.
- [ ] O guia `modelo_ieee.md` ainda descreve um esqueleto de quatro páginas e sete referências.
- [ ] M6 não possui faixa de pontuação para valores maiores ou iguais a 99% e menores que 100%.
- [ ] Classes A/B/C não cobrem todos os resultados possíveis; por exemplo, IQM ≥ 3,25 com alguma característica entre 2,5 e 3,0 pode ficar sem classificação.
- [ ] Formalizar o tratamento de tarefas sem concluintes ou sem tempo de referência válido.
- [ ] Completar a verificação das fontes normativas e do livro PSM, sem tratar metadados como leitura integral.
- [ ] Conferir rubricas nos PDFs oficiais da disciplina, indisponíveis neste repositório.

## Fechamento da validação

- [ ] Registrar responsável e data da conferência.
- [ ] Resolver divergências antes de aplicar os critérios na coleta.
- [ ] Conferir chamadas, legendas e fontes das 11 tabelas e três figuras.
- [ ] Manter o PDF em até dez páginas, incluindo referências e apêndice.
- [ ] Manter as seções futuras da Entrega 2 desativadas nesta versão.

**Responsável:** ______ · **Data:** ______ · **Revisão do artigo:** ______ · **Revisão da GitPage:** ______
