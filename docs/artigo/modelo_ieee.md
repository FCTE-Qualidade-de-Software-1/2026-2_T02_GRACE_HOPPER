# Artigo IEEE sobre qualidade do i-Educar

O [artigo em PDF](main.pdf) e a [fonte LaTeX editável](main.tex) apresentam a estrutura do estudo e o planejamento atualizado. Os protocolos descritos ainda serão executados; resultados e conclusões empíricas permanecem pendentes.

## Base documental e atualização

Esta revisão acompanha as alterações incorporadas pelo PR #20, no commit `ff53da3`, incluindo identificação da equipe, propósito e priorização da avaliação e os protocolos de compatibilidade e interação. As duas referências internas do artigo apontam para essa revisão dos documentos, permitindo recuperar a base utilizada. A bibliografia inclui também o software avaliado e as fontes conceituais externas.

| Fonte | Conteúdo incorporado |
| --- | --- |
| [README](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/blob/ff53da3/README.md) e [planejamento PC1, seção 3](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md#3-gestao-de-recursos-esforco-e-custos-psmcid-e-criterio-ag-c5) | Os seis autores, na ordem registrada pela equipe |
| [Planejamento PC1, seção 2.1](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md#21-fase-1-estabelecer-os-requisitos-da-avaliacao) | Natureza diagnóstica, decisões apoiadas e priorização por impacto, risco e viabilidade |
| [Framework GQM, seções 2, 3 e 4](../gqm_evaluation_framework.md) | Questões, procedimentos, instrumentos e limiares atuais |

**Autores:** Arthur Soares Parente; Fábio Santos Araujo; Gabriel Barbaceli; Gustavo Silva Rodrigues; Ítalo Alves Sampaio de Oliveira; Ricardo Lucas Winchello Vieira Branco. Os contatos acadêmicos ainda precisam ser preenchidos.

Para identificadores, procedimentos e limiares, o artigo segue as definições detalhadas do framework GQM. O quadro-resumo da seção 2.2 e alguns trechos gerais do planejamento PC1 ainda usam métricas ou escopos anteriores; eles não substituem o protocolo detalhado. Em particular, Educacenso/INEP está fora de G1, e a qualidade em uso considera matrícula e diário, com comparação relativa de tempo.

## Modelo adotado

Adota-se o **IEEE Conference** fornecido pela equipe: [PDF de referência](model/conference_101719.pdf) e [classe IEEEtran](model/IEEEtran.cls), versão 1.8b. O artigo usa essa classe no modo `conference`, sem modificações. O [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/authoring-tools-and-templates/) é a fonte oficial de templates.

O arquivo [main.tex](main.tex) é o único texto de trabalho do artigo. Usa duas colunas, títulos de seções e referências numéricas controlados pela classe. Não alterar margens, fontes ou espaçamento para acomodar conteúdo.

```text
docs/artigo/
├── main.tex                  # Esqueleto editável do artigo
├── main.pdf                  # PDF compilado do artigo
├── modelo_ieee.md            # Orientações e rastreabilidade
├── .gitignore               # Arquivos auxiliares de compilação
└── model/
    ├── conference_101719.pdf # Referência visual original
    └── IEEEtran.cls          # Classe original usada na compilação
```

O exemplo-fonte, sua imagem demonstrativa e o manual auxiliar foram removidos. A pasta `model` conserva apenas o referencial visual e a dependência efetivamente usada.

**Título proposto:** Avaliação da Qualidade de Software da Plataforma i-Educar: um Estudo dos Módulos de Matrícula e Lançamento de Notas.

O texto será inicialmente escrito em português para a disciplina. A configuração de página segue o modelo fornecido: papel Letter, padrão da classe, sem a opção `a4paper` da base anterior. Idioma, tamanho do papel, limite de páginas, identificação dos autores e exigência de resumo em inglês devem ser conferidos com a professora ou com o evento de destino antes da entrega; não há limite de páginas universal do IEEE.

## Estrutura e rastreabilidade

| Seção do artigo | Conteúdo | Base no repositório |
| --- | --- | --- |
| Resumo e palavras-chave | Problema, objetivo, método e, após coleta, principais resultados | Síntese do artigo |
| Introdução | Contexto, motivação, objetivo e delimitação | [Planejamento PC1](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md) |
| Fundamentação e trabalhos relacionados | Modelos de qualidade, GQM e comparação com estudos existentes | Catálogos oficiais ISO, referência original de GQM e estudos relacionados ainda a selecionar |
| Metodologia | Objeto, versão/commit, ambiente, priorização, questões, métricas, sessões de uso, critérios e coleta | [Planejamento PC1](../relatorio_de_planejamento_ponto_de_controle_1_i_educar.md) e [framework GQM](../gqm_evaluation_framework.md) |
| Resultados | Medições, amostras, evidências e julgamento | Evidências a coletar; não apresentar metas como resultados |
| Discussão | Respostas às questões, implicações e recomendações | Interpretação das medições |
| Ameaças à validade | Limites de amostra, instrumentos, ambiente e generalização | Condições efetivas da avaliação |
| Conclusão | Resposta ao objetivo e próximos passos | Síntese sustentada pelas evidências |
| Declaração de uso de IA | Ferramentas, tarefas e revisão humana efetivamente realizadas | Registro da equipe |
| Referências | Somente fontes consultadas e citadas | Bibliografia em estilo IEEE |

O site mantém o detalhamento do planejamento, GQM, gestão e evidências. O artigo apresenta a síntese científica e aponta para os artefatos complementares. A versão e a arquitetura do i-Educar descritas nos documentos existentes devem ser verificadas no commit efetivamente avaliado antes de serem afirmadas no artigo.

### Rastreabilidade dos objetivos e resultados

Os identificadores são os do [framework GQM](../gqm_evaluation_framework.md). As divisões M7a/M7b e M14a/M14b seguem sua tabela de limiares. As âncoras abaixo são os `labels` LaTeX do artigo; as referências entre metodologia, resultados e discussão usam `\ref`.

| Objetivo | Questão → métrica(s) | Metodologia → resultados | Origem no GQM |
| --- | --- | --- | --- |
| Priorização | Impacto, risco, viabilidade e pesos das características | `sec:priorizacao` → `res:julgamento` | Planejamento PC1, seção 2.1, item 4 e Tabela 2 |
| G1 — Compatibilidade | Q1.1 → M1 (isolamento por configuração); Q1.2 → M2 (contrato da API) | `met:g1` → `res:g1` | Seções 2, 3.1 e 4 |
| G2 — Confiabilidade | Q2.1 → M3; Q2.2 → M4 e M5; Q2.3 → M6 | `met:g2` → `res:g2` | Seções 2, 3.2, 4 e 5.1 |
| G3 — Manutenibilidade | Q3.1 → M7a e M7b; Q3.2 → M8; Q3.3 → M9; Q3.4 → M10; Q3.5 → M11 | `met:g3` → `res:g3` | Seções 2, 3.3 e 4 |
| G4 — Interação e qualidade em uso | Q4.1 → M12 (bloqueio de entradas); Q4.2 → M13 (causa e ação); Q4.3 → M14a e M14b (tempo relativo); Q4.4 → M15 (sucesso em T1 e T2) | `met:g4` e `sec:sessoes` → `res:g4` | Seções 2, 3.4 e 4 |
| Julgamento | Critérios eliminatórios M3, M4 e M12; índices por característica e global | `sec:julgamento` → `res:julgamento` | Seções 4 e 5 |

Cada medição deverá registrar objetivo, questão, métrica, cenário ou amostra, valor, unidade, critério aplicado, localização da evidência, versão do software, data e responsável. Os resultados ficam pendentes até a coleta. Dados indisponíveis não são convertidos em zero nem classificados como aprovação ou reprovação.

Antes de aplicar os critérios, fixar a revisão do GQM e conferir a cobertura dos limiares e regras de julgamento. O esqueleto não redefine os pesos, as fórmulas ou os critérios do documento de origem.

### Protocolos incorporados

**Propósito e priorização.** A avaliação é independente e diagnóstica. Apoia decisões de adoção e atualização pelas Secretarias, refatoração pelos mantenedores, integração pelas equipes de TI e capacitação das equipes escolares. A priorização usa impacto × risco, condicionada à viabilidade mínima de 3 em escala de 1 a 5. Manutenibilidade e confiabilidade recebem 30% cada; compatibilidade, 20%; interação e uso, 20%, com capacidade de interação obrigatória na disciplina. Segurança e desempenho em escala de produção não são avaliados.

**G1.** M1 passa a medir a proporção de recursos isoláveis por configuração, confirmados em teste com uma segunda instância no mesmo host. M2 mede endpoints conformes em todos os casos previstos, com contrato oficial ou JSON Schema derivado e versionado antes da execução. Devem ser preservados inventário, configurações, coleção de requisições e relatórios. Exportação Educacenso/INEP e integrações que dependam de credenciais de produção ficam fora do recorte.

**G4 — produto.** M12 usa no mínimo três cenários por tipo de entrada inválida, executados pela interface e pela API, com conferência da persistência no banco. O bloqueio precisa apresentar mensagem sem erro 500, tela em branco ou perda dos demais dados. M13 avalia causa e ação corretiva nas mensagens de M12, por dois classificadores independentes, com registro do consenso.

**G4 — uso.** O protocolo prevê no mínimo cinco voluntários iniciantes, TCLE, dados fictícios e registros anonimizados. T1 é matrícula e enturmação de aluno já cadastrado; T2 é lançamento de notas de um componente para dez alunos. As tarefas seguem essa ordem, com gravação de tela e áudio e sem auxílio do avaliador. O tempo de referência é a média de três execuções por um integrante treinado. M14 mantém os tempos em minutos, mas M14a/M14b são julgadas pela razão entre a média dos concluintes e o tempo de referência. M15 considera a primeira submissão correta nas duas tarefas, com verificação no banco.

### Limiares alterados no GQM

| Métrica e unidade de julgamento | Crítico | Regular | Bom | Excelente |
| --- | --- | --- | --- | --- |
| M1 e M2 — percentual | < 70% | ≥ 70% e < 85% | ≥ 85% e < 100% | 100% |
| M14a e M14b — razão de tempo, adimensional | > 3 | > 2 e ≤ 3 | > 1,5 e ≤ 2 | ≤ 1,5 |
| M15 — percentual de sucesso em T1 e T2 | < 50% | ≥ 50% e < 70% | ≥ 70% e < 90% | ≥ 90% |

As demais métricas e os critérios eliminatórios M3, M4 e M12 seguem o framework. Antes da coleta, é necessário definir o tratamento de tarefas sem concluintes ou sem tempo de referência válido, além de registrar a versão exata do software e dos instrumentos.

## Edição e compilação

No Overleaf, carregar `main.tex` e a pasta `model` em um projeto, mantendo essa estrutura a partir da raiz. Selecionar `main.tex` como documento principal e **pdfLaTeX** como compilador. O próprio `main.tex` inclui `model/` na busca de arquivos para localizar a classe fornecida. O ambiente deve ter suporte de idioma português.

Localmente, usar TeX Live ou equivalente com as fontes exigidas por `IEEEtran`, `babel` com português, `fontenc`, `inputenc` e `url`. A classe já está incluída no repositório. A partir da raiz do repositório, executar os comandos abaixo. O PDF e os arquivos auxiliares serão gravados em uma pasta temporária:

```bash
cd docs/artigo
artigo_build_dir="$(mktemp -d /tmp/ieducar-artigo-XXXXXX)"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$artigo_build_dir" main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$artigo_build_dir" main.tex
printf 'PDF: %s/main.pdf\n' "$artigo_build_dir"
# Após as duas passagens concluírem sem erro, atualizar o PDF da página:
cp "$artigo_build_dir/main.pdf" main.pdf
```

Executar a segunda passagem apenas após o sucesso da primeira. Se houver erro de dependência, consultar o log antes de repetir. A compilação depende também das fontes Times utilizadas pela classe.

As referências usam `thebibliography`, com numeração IEEE pela ordem de primeira citação. Todas as entradas são citadas no texto. Se a bibliografia crescer, migrar para BibTeX com `\bibliographystyle{IEEEtran}` e incluir o arquivo de estilo necessário.

### Composição da bibliografia

As três entradas anteriores correspondiam somente ao repositório da equipe, ao framework GQM e ao planejamento PC1. Elas registravam a origem do plano, mas ainda não constituíam a fundamentação externa do artigo. A entrada genérica do repositório da equipe foi substituída pela fonte oficial do software avaliado; os dois documentos específicos foram mantidos para identificar os critérios próprios do projeto.

| Fonte | Papel no artigo |
| --- | --- |
| [i-Educar — repositório oficial](https://github.com/portabilis/i-educar) | Identificação do software avaliado; versão e commit da execução ainda devem ser fixados |
| Framework GQM e planejamento PC1, revisão `ff53da3` | Rastreabilidade dos protocolos, pesos, limiares e decisões da equipe |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Modelo de qualidade de produto |
| [ISO/IEC 25019:2023](https://www.iso.org/standard/78177.html) | Modelo de qualidade em uso |
| [ISO/IEC 25040:2024](https://www.iso.org/standard/83467.html) | Framework de avaliação da qualidade; título e endereço oficial conferidos |
| [Basili, Caldiera e Rombach (1994)](https://www.cs.umd.edu/~basili/publications/technical/T89.pdf) | Referência original da abordagem GQM; dados bibliográficos conferidos na [lista de publicações do autor](https://www.cs.umd.edu/~basili/papers.html) |

A bibliografia atual contém **sete entradas: cinco fontes externas e dois documentos internos**. As normas foram identificadas pelos catálogos públicos da ISO; a revisão não equivale à leitura de seus textos integrais. Os parágrafos normativos limitam-se ao escopo publicamente descrito. Pesos e limiares continuam atribuídos à equipe. A seleção e a leitura de estudos relacionados permanecem pendentes.

Antes da entrega, substituir todos os campos `[PREENCHER: ...]`, revisar as citações, citar cada tabela e figura no texto e indicar sua fonte. Nas legendas, usar título de tabela acima e legenda de figura abaixo. Não inserir selos de publicação, ISBN ou copyright de um evento sem as instruções correspondentes.

## Validação desta estrutura

- A verificação do site (`bash scripts/docs/check_site.sh`) passou, incluindo o build estrito e as verificações de links e fórmulas.
- A revisão estática conferiu os identificadores das seções, as referências internas, as citações, os ambientes LaTeX, os links locais do guia e os dois arquivos preservados em `model`.
- O artigo compilou com pdfLaTeX em duas passagens, gerando quatro páginas em Letter. As sete entradas bibliográficas são distintas, estão citadas na ordem de primeira ocorrência e não apresentam referências indefinidas. Não há caixas excedendo a largura das colunas. O PDF atualizado está disponível no início desta página.
- O ambiente ainda emite avisos sobre a busca da classe na subpasta `model`, padrões de hifenização em português não pré-carregados e espaçamento em algumas linhas. Esses avisos não impediram a geração do PDF; a hifenização deve ser conferida na revisão editorial final.

**Estado:** esqueleto de escrita; os resultados da avaliação ainda não foram incorporados.
