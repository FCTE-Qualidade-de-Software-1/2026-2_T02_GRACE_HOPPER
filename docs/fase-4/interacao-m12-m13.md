# Capacidade de interação: proteção contra erros e autodescritividade (Gate M12 e M13)

Resultado da instrumentação e execução da bateria de testes de entradas inválidas e da auditoria independente por pares das mensagens de validação sobre o commit oficial congelado do **i-Educar 2.12**, em cumprimento à [Issue #45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45). As definições conceituais, fórmulas e limiares derivam do [Framework GQM](../gqm_evaluation_framework.md) (G4 — Capacidade de Interação) e o roteiro segue a Tabela 4 do [Plano de medição e testes](../plano_medicao_testes.md).

---

## 1. Execução e Integridade Metodológica

Em conformidade com os princípios de auditabilidade e reprodutibilidade da **ISO/IEC 25040:2024** e da **ISO/IEC 25010:2023**, o universo de teste foi estruturado em um catálogo com 12 cenários cobrindo as quatro categorias operacionais de risco de erro do usuário (3 cenários por categoria: C1 a C4). O catálogo foi congelado com digest criptográfico SHA-256 antes da execução e auditoria.

**Tabela 1 — Dados da execução da avaliação de interação e proteção contra erros**

| Item | Valor |
| :--- | :--- |
| Produto avaliado | `portabilis/i-educar`, commit `7903a3efc7689942ee700007f86ed581023aad27` (branch `2.12`) |
| Instrumentos de teste | `scripts/uso/avaliar_m12_m13.py`, testes de API REST (Laravel Test / Pest) e inspeção de código |
| Data da apuração | 12/11/2026 |
| Responsável pela trilha | Gabriel Barbaceli (`@Nibaacriba`) — Trilha B |
| Revisor por pares | Ítalo Sampaio (`@ItaloSamP`) — Trilha D |
| Manifesto / Catálogo congelado | [`catalogo_cenarios_m12.json`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/blob/main/evidencias/g4_interacao_uso/m12_catalogo/catalogo_cenarios_m12.json) (SHA-256: `c3993682e35c6c19570f03d4221a3f52dbd087312af8a502e3b08b926bf83f5d`) |
| Evidências geradas | [`m12_ippe.csv`](../evidencias/g4_interacao_uso/m12_ippe.csv), [`m12_ippe_execucao.log`](../evidencias/g4_interacao_uso/m12_ippe_execucao.log) e [`m13_admv.json`](../evidencias/g4_interacao_uso/m13_admv.json) |

*Fonte: elaborado pelos autores.*

---

## 2. Resultados Consolidados

A Tabela 2 sintetiza os resultados empíricos obtidos para o Gate Binário M12 e para a métrica gradual M13, o enquadramento nos limiares normativos e a validação das hipóteses acadêmicas de pesquisa.

**Tabela 2 — Resultados, veredito dos gates e julgamento de hipóteses (G4)**

| Métrica / Gate | Valor medido | Nível ($S_i$) / Veredito | Hipótese associada | Julgamento da hipótese |
| :--- | :---: | :---: | :--- | :--- |
| **Gate M12** — $\text{IPPE}$ (Proteção contra Erros) | **100,0%** | **APROVADO** (Gate Binário) | H4.1: O sistema bloqueia 100% dos cenários inválidos previstos sem persistir dados corrompidos nem retornar erro HTTP 500 | **Confirmada:** 12 de 12 cenários bloqueados amigavelmente sem efeitos colaterais no banco |
| **M13** — $\text{ADMV}$ (Autodescritividade) | **83,33%** | Regular ($S=2$, faixa $[80{,}0\%, 90{,}0\%)$) | H4.2: Entre 80% e 90% das mensagens informam causa e ação corretiva, com mensagens genéricas residuais no núcleo legado | **Confirmada:** 10 de 12 mensagens com causa e ação claras; 2 mensagens residuais no legado |

*Fonte: elaborado pelos autores a partir da execução do catálogo de cenários no commit `7903a3e`.*

---

## 3. Gate Binário M12 — Índice de Proteção contra Erros do Usuário (IPPE)

A métrica M12 atua como o **Gate Binário eliminatório** da característica Capacidade de Interação. Ela verifica se o sistema é capaz de interceptar requisições com dados inconsistentes ou violações de prazos regulamentares antes de persistir alterações indesejadas no banco de dados.

$$
\text{IPPE} = \dfrac{N_{\text{cenários bloqueados amigavelmente}}}{N_{\text{cenários inválidos submetidos}}} \times 100\%
$$

O critério de **bloqueio amigável** exige a satisfação estrita e simultânea de quatro condições:
1. Rejeição com status HTTP 422 (*Unprocessable Entity*) ou tratamento controlado de exceção de domínio.
2. Nenhuma alteração persistida nas tabelas operacionais do PostgreSQL (`modules.nota_componente_curricular`, `modules.nota_aluno`, `modules.falta_aluno`, `pmieducar.matricula_turma`).
3. Ausência absoluta de erros de servidor não tratados (HTTP 500) ou telas em branco (*white screen of death*).
4. Retorno de mensagem descritiva orientada ao usuário no corpo JSON ou através do componente `Portabilis_Messenger`.

A Tabela 3 detalha a execução dos 12 cenários previstos nas quatro categorias do catálogo.

**Tabela 3 — Detalhamento da execução dos 12 cenários inválidos de teste (Gate M12)**

| ID | Categoria | Cenário Inspecionado / Testado | Componente / Exception Alvo | Status HTTP | Bloqueio Amigável | Persistência Indesejada | Erro 500 |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `C1.1` | C1 — Nota fora da faixa | Nota 11,0 acima da nota máxima geral configurada (10,0) | `NotasController.php` / `ScoreGreaterThanMaxAllowed` (cód. 1003) | 422 | SIM | NÃO | NÃO |
| `C1.2` | C1 — Nota fora da faixa | Nota negativa -1,5 abaixo da nota mínima geral (0,0) | `NotasController.php` / `ScoreLesserThanMinAllowed` (cód. 1004) | 422 | SIM | NÃO | NÃO |
| `C1.3` | C1 — Nota fora da faixa | Nota de exame 10,5 acima do limite de exame final (10,0) na etapa Rc | `NotasController.php` / `ExamScoreGreaterThanMaxAllowed` (cód. 1005) | 422 | SIM | NÃO | NÃO |
| `C2.1` | C2 — Etapa/ano bloqueado | Lançamento em ano letivo encerrado (andamento=2) com bloqueio escolar | `DiarioApiController.php:validatesCanChangeDiarioForAno` | 422 | SIM | NÃO | NÃO |
| `C2.2` | C2 — Etapa/ano bloqueado | Lançamento fora da janela de datas institucionais (`LegacySchoolYearLock`) | `DiarioApiController.php:validatesCanChangeDiarioForAno` | 422 | SIM | NÃO | NÃO |
| `C2.3` | C2 — Etapa/ano bloqueado | Lançamento fora do período configurado para a etapa do curso | `DiarioApiController.php:validatesPeriodoLancamentoFaltasNotas` | 422 | SIM | NÃO | NÃO |
| `C3.1` | C3 — Menção inválida | Menção alfanumérica 'ÓTIMO' não constante na tabela de arredondamento | `LegacyValueRoundingTable.php` / `DiarioApiController.php` | 422 | SIM | NÃO | NÃO |
| `C3.2` | C3 — Menção inválida | Envio de nota numérica contínua em disciplina de avaliação conceitual | `DiarioApiController.php:validatesRegraAvaliacaoHasNota` | 422 | SIM | NÃO | NÃO |
| `C3.3` | C3 — Menção inválida | Submissão sem `matricula_id` nem `componente_curricular_id` | `DiarioApiController.php:validatesPresenceOfMatriculaId...` | 422 | SIM | NÃO | NÃO |
| `C4.1` | C4 — Conflito de matrícula | Enturmação em turma sem vagas remanescentes (capacidade esgotada) | `EnrollmentService.php` / `NoVacancyException` | 422 | SIM | NÃO | NÃO |
| `C4.2` | C4 — Conflito de matrícula | Data de enturmação anterior à data de início do ano acadêmico da turma | `EnrollmentService.php` / `EnrollDateBeforeAcademicYearException` | 422 | SIM | NÃO | NÃO |
| `C4.3` | C4 — Conflito de matrícula | Tentativa de criar segunda enturmação ativa concomitante para mesma matrícula | `EnrollmentService.php` / `ExistsActiveEnrollmentException` | 422 | SIM | NÃO | NÃO |

*Fonte: `evidencias/g4_interacao_uso/m12_ippe.csv` e `m12_ippe_execucao.log`. Elaborado pelos autores.*

### 3.1 Veredito do Gate M12
Com 12 cenários bloqueados amigavelmente dentre os 12 submetidos:

$$
\text{IPPE} = \dfrac{12}{12} \times 100\% = 100{,}0\%
$$

O **Gate Binário M12 é formalmente APROVADO**. A hipótese de pesquisa **H4.1 é Confirmada**, comprovando que a camada de controle e os serviços de domínio do i-Educar interceptam robustamente as entradas inválidas de notas, datas e matrículas antes de qualquer escrita no banco de dados.

---

## 4. M13 — Autodescritividade das Mensagens de Validação (ADMV)

A métrica M13 mensura a qualidade e a utilidade prática das mensagens de erro apresentadas ao usuário quando um bloqueio ocorre. Segundo a **ISO/IEC 25010:2023** (*Self-descriptiveness*), uma mensagem autodescritiva deve satisfazer cumulativamente dois critérios essenciais:
1. **Informar a causa clara do erro:** explicar de maneira compreensível o motivo pelo qual a operação foi rejeitada.
2. **Indicar a ação corretiva:** instruir ou orientar o usuário sobre como proceder para corrigir o dado ou solucionar o impedimento.

$$
\text{ADMV} = \dfrac{N_{\text{mensagens com causa e ação}}}{N_{\text{mensagens de erro avaliadas}}} \times 100\%
$$

### 4.1 Processo de Auditoria Independente com Dupla Checagem
Cada mensagem retornada nos 12 cenários de M12 foi submetida à avaliação independente e cega de dois integrantes da equipe:
- **Avaliador 1:** Gabriel Barbaceli (`@Nibaacriba`), responsável pela Trilha B.
- **Avaliador 2:** Ítalo Sampaio (`@ItaloSamP`), revisor por pares da Trilha D.

As discrepâncias iniciais foram debatidas e solucionadas em reunião de consenso técnico registrada. A Tabela 4 apresenta o inventário completo das mensagens, as classificações individuais e o consenso homologado.

**Tabela 4 — Auditoria cruzada de mensagens de validação (Avaliador 1 vs. Avaliador 2 vs. Consenso)**

| ID | Mensagem Exibida pelo Sistema | Avaliador 1 (Gabriel) | Avaliador 2 (Ítalo) | Consenso Homologado | Classificação Final |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `C1.1` | *"A nota 11 está acima da configurada para nota máxima geral que é 10."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C1.2` | *"A nota -1.5 está abaixo da configurada para nota mínima geral que é 0."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C1.3` | *"A nota 10.5 está acima da configurada para nota máxima para exame que é 10."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C2.1` | *"O ano letivo '2023' está encerrado, esta escola está configurada para não permitir alterar o diário de anos letivos encerrados."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** *(consenso: delimita a regra escolar e o ano objeto de ação)* |
| `C2.2` | *"O lançamento de notas nessa instituição está bloqueado nesta data."* | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: NÃO | **Parcialmente autodescritiva** *(legado: omite janela temporal válida)* |
| `C2.3` | *"Não é permitido realizar esta alteração fora do período de lançamento de notas/faltas."* | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: NÃO | **Parcialmente autodescritiva** *(legado: omite datas de vigência da etapa)* |
| `C3.1` | *"Menção conceitual 'ÓTIMO' não é válida para a tabela de arredondamento da regra de avaliação."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C3.2` | *"Nota não lançada, pois a regra de avaliação não utiliza nota."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C3.3` | *"É necessário receber matricula_id ou componente_curricular_id."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C4.1` | *"Não há vagas na turma \"6º Ano A\" #101."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C4.2` | *"A data de enturmação 10/01/2026 é anterior ao início do ano acadêmico 01/02/2026."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C4.3` | *"Existe outra enturmação ativa para a matrícula 501."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |

*Fonte: `evidencias/g4_interacao_uso/m13_admv.json`. Elaborado pelos autores.*

### 4.2 Julgamento da Hipótese H4.2
- **Percentual de Autodescritividade:** Das 12 mensagens auditadas, **10 atendem cumulativamente aos requisitos de causa e ação corretiva** ($N_{\text{com causa e ação}} = 10$).
- Todas as 12 mensagens (100%) informam com clareza a causa do bloqueio.
- As mensagens `C2.2` e `C2.3` falham no critério de ação corretiva por constituírem mensagens secas do legado procedimental (`DiarioApiController.php`), as quais comunicam que o lançamento está impedido, porém não informam a janela de datas autorizada nem fornecem instrução de contato com a coordenação pedagógica.

$$
\text{ADMV} = \dfrac{10}{12} \times 100\% = 83{,}33\%
$$

O valor apurado de **$83{,}33\%$ enquadra-se no Nível Regular ($S=2$)**, situado dentro da faixa $[80{,}0\%, 90{,}0\%)$ prevista pelo Framework GQM. **A hipótese H4.2 é formalmente Confirmada**, ratificando a premissa de que a maior parte dos fluxos é amigável e orientada à correção, subsistindo um resíduo de mensagens genéricas na camada de validação temporal herdada do código legado.

---

## 5. Impacto no Julgamento Final da Release E2 (Fase 5)

A aprovação do **Gate Binário M12 (IPPE = 100,0%)** é condição mandatória para que o software possa aspirar às classificações **Classe A** ou **Classe B** na Fase 5 da ISO/IEC 25040:2024:
- Se o Gate M12 houvesse falhado, o produto receberia imediatamente a **Classificação C (Reprovado / Bloqueado)**, impedindo o avanço para a etapa de qualidade em uso com participantes humanos.
- O resultado favorável permite prosseguir com as sessões experimentais de qualidade em uso (M14a, M14b e M15) sem risco de corrupção da base relacional.
- Para a métrica M13, o enquadramento em nível Regular ($S=2$) não bloqueia o release na Classe B, mas impõe a inclusão de um item de melhoria no backlog de manutenibilidade: a reestruturação das validações temporais em `DiarioApiController.php` para que passem a retornar as datas de início e fim da janela de lançamento.

---

## 6. Procedimento de Reprodução

Para reproduzir integralmente as checagens e relatórios a partir da raiz do repositório:

```bash
# 1. Conferir a integridade do catálogo congelado de cenários
cd evidencias/g4_interacao_uso/m12_catalogo && shasum -c manifesto.sha256 && cd ../../..

# 2. Executar a suíte de testes unitários do avaliador
python3 -m unittest scripts/uso/test_avaliar_m12_m13.py

# 3. Executar o motor de avaliação de interação e gerar evidências
python3 scripts/uso/avaliar_m12_m13.py \
  --path=./i-educar-src \
  --output-dir=docs/evidencias/g4_interacao_uso

# 4. Validar aderência do site e links de documentação
bash scripts/docs/check_site.sh
```
