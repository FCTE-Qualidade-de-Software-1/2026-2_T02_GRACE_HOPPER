# Capacidade de interação: proteção contra erros e autodescritividade (Gate M12 e M13)

Resultado da instrumentação e execução da bateria de testes de entradas inválidas e da auditoria independente por pares das mensagens de validação sobre o commit oficial congelado do **i-Educar 2.12**, em cumprimento à [Issue #45](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/45). As definições conceituais, fórmulas e limiares derivam do [Framework GQM](../gqm_evaluation_framework.md) (G4 — Capacidade de Interação) e o roteiro segue a Tabela 4 do [Plano de medição e testes](../plano_medicao_testes.md).

---

## 1. Execução e Integridade Metodológica

Em conformidade com os princípios de auditabilidade e reprodutibilidade da **ISO/IEC 25040:2024** e da **ISO/IEC 25010:2023**, o universo de teste foi estruturado em um catálogo com 12 cenários cobrindo as quatro categorias operacionais de risco de erro do usuário (3 cenários por categoria: C1 a C4). O catálogo foi congelado com digest criptográfico SHA-256 antes da execução e auditoria.

**Tabela 1 — Dados da execução da avaliação de interação e proteção contra erros**

| Item | Valor |
| :--- | :--- |
| Produto avaliado | `portabilis/i-educar`, commit `7903a3efc7689942ee700007f86ed581023aad27` (branch `2.12`) |
| Instrumentos de teste | Execução HTTP real em instância Docker (`PHP 8.5.11` + `PostgreSQL 16` + `Redis`) com conferência SQL antes/depois + validação automatizada por `scripts/uso/avaliar_m12_m13.py` |
| Data da reexecução real | 14/11/2026 |
| Responsável pela trilha | Gabriel Barbaceli (`@Nibaacriba`) — Trilha B |
| Revisor por pares | Ítalo Sampaio (`@ItaloSamP`) — Trilha D |
| Manifesto / Catálogo congelado | `evidencias/g4_interacao_uso/m12_catalogo/catalogo_cenarios_m12.json` (SHA-256: `65bd5f73aed06acfb6fc02d207e0ddb717e6681aab677d4095b46b4469ad413c`) |
| Capturas HTTP/SQL brutas | 12 arquivos JSON em `docs/evidencias/g4_interacao_uso/capturas_m12/` (`C1.1.json` a `C4.3.json`) |
| Evidências geradas | [`m12_ippe.csv`](../evidencias/g4_interacao_uso/m12_ippe.csv), [`m12_ippe_execucao.log`](../evidencias/g4_interacao_uso/m12_ippe_execucao.log) e [`m13_admv.json`](../evidencias/g4_interacao_uso/m13_admv.json) |

*Fonte: elaborado pelos autores.*

---

## 2. Resultados Consolidados

A Tabela 2 sintetiza os resultados empíricos obtidos na execução real contra o i-Educar + PostgreSQL para o Gate Binário M12 e para a métrica gradual M13, o enquadramento nos limiares normativos e o julgamento das hipóteses associadas.

**Tabela 2 — Resultados, veredito dos gates e julgamento de hipóteses (G4)**

| Métrica / Gate | Valor medido | Nível ($S_i$) / Veredito | Hipótese associada | Julgamento da hipótese |
| :--- | :---: | :---: | :--- | :--- |
| **Gate M12** — $\text{IPPE}$ (Proteção contra Erros) | **100,0%** | **APROVADO** (Gate Binário) | H4.1: O sistema bloqueia 100% dos cenários inválidos previstos sem persistir dados corrompidos nem retornar erro HTTP 500 | **Confirmada:** 12 de 12 cenários bloqueados em runtime sem alteração de contagem SQL (`delta = 0`) nem HTTP 500 |
| **M13** — $\text{ADMV}$ (Autodescritividade) | **75,00%** | Crítico ($S=1$, faixa $< 80{,}0\%$) | H4.2: Entre 80% e 90% das mensagens informam causa e ação corretiva, com mensagens genéricas residuais no núcleo legado | **Refutada:** 9 de 12 mensagens atingiram causa + ação (`75,00% < 80,0%`); além de `C2.2` e `C2.3`, o FormRequest de `POST /api/v2/notas` (`C3.1`) retornou mensagem genérica sem ação corretiva |

*Fonte: elaborado pelos autores a partir da execução real do catálogo de cenários no commit `7903a3e`.*

---

## 3. Gate Binário M12 — Índice de Proteção contra Erros do Usuário (IPPE)

A métrica M12 atua como o **Gate Binário eliminatório** da característica Capacidade de Interação. Ela verifica se o sistema intercepta requisições com dados inconsistentes ou violações regulamentares antes de persistir alterações indesejadas no PostgreSQL.

$$
\text{IPPE} = \dfrac{N_{\text{cenários bloqueados amigavelmente}}}{N_{\text{cenários inválidos submetidos}}} \times 100\%
$$

O critério de **bloqueio amigável** exige a satisfação estrita e simultânea de quatro condições comprovadas na captura bruta de cada cenário:
1. Rejeição controlada conforme o protocolo do endpoint real: HTTP `422` com erros de validação na API v2 (`/api/v2/notas`), HTTP `200` com `any_error_msg: true` e mensagem no array `msgs` na API legada (`DiarioApiController`), ou HTTP `302 -> 200` com mensagem de flash de erro no fluxo web (`EnrollmentController`).
2. Nenhuma alteração persistida nas tabelas operacionais do PostgreSQL (`contagem_antes == contagem_depois`, `delta = 0` em `modules.nota_componente_curricular`, `modules.nota_exame`, `modules.nota_aluno` e `pmieducar.matricula_turma`).
3. Ausência absoluta de erros de servidor não tratados (HTTP 500) ou telas em branco (*white screen of death*).
4. Retorno de mensagem descritiva orientada ao usuário e vinculada pelo hash SHA-256 do corpo da resposta bruta.

A Tabela 3 detalha a execução real dos 12 cenários nas quatro categorias do catálogo.

**Tabela 3 — Detalhamento da execução real dos 12 cenários inválidos de teste (Gate M12)**

| ID | Categoria | Endpoint e Cenário Executado | Status HTTP | Tabela SQL (`antes -> depois`) | Bloqueio Amigável | Captura Bruta |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| `C1.1` | C1 — Nota fora da faixa | `POST /api/v2/notas` com `nota = 11.0` (> máx 10,0) | 422 | `modules.nota_componente_curricular` (`2 -> 2`, delta `0`) | SIM | [`C1.1.json`](../evidencias/g4_interacao_uso/capturas_m12/C1.1.json) |
| `C1.2` | C1 — Nota fora da faixa | `POST /api/v2/notas` com `nota = -1.5` (< mín 0,0) | 422 | `modules.nota_componente_curricular` (`2 -> 2`, delta `0`) | SIM | [`C1.2.json`](../evidencias/g4_interacao_uso/capturas_m12/C1.2.json) |
| `C1.3` | C1 — Nota fora da faixa | `POST /api/v2/notas` na etapa `Rc` com `nota = 10.5` (> teto exame 10,0) | 422 | `modules.nota_exame` (`0 -> 0`, delta `0`) | SIM | [`C1.3.json`](../evidencias/g4_interacao_uso/capturas_m12/C1.3.json) |
| `C2.1` | C2 — Etapa/ano bloqueado | `GET /module/Avaliacao/diarioApi` (`resource=matriculas`) em ano encerrado (`2023`) com escola configurada para bloquear edição | 200 (`any_error_msg: true`) | `modules.nota_aluno` (`8 -> 8`, delta `0`) | SIM | [`C2.1.json`](../evidencias/g4_interacao_uso/capturas_m12/C2.1.json) |
| `C2.2` | C2 — Etapa/ano bloqueado | `GET /module/Avaliacao/diarioApi` (`resource=matriculas`) em data bloqueada (`LegacySchoolYearLock`) | 200 (`any_error_msg: true`) | `modules.nota_aluno` (`8 -> 8`, delta `0`) | SIM | [`C2.2.json`](../evidencias/g4_interacao_uso/capturas_m12/C2.2.json) |
| `C2.3` | C2 — Etapa/ano bloqueado | `GET /module/Avaliacao/diarioApi` (`resource=nota&oper=post`) fora do período de lançamento por perfil sem `POST_OUT_PERIOD` | 200 (`any_error_msg: true`) | `modules.nota_componente_curricular` (`2 -> 2`, delta `0`) | SIM | [`C2.3.json`](../evidencias/g4_interacao_uso/capturas_m12/C2.3.json) |
| `C3.1` | C3 — Menção inválida | `POST /api/v2/notas` submetendo texto conceitual `nota = "ÓTIMO"` (`PostNotasRequest`) | 422 | `modules.nota_componente_curricular` (`2 -> 2`, delta `0`) | SIM | [`C3.1.json`](../evidencias/g4_interacao_uso/capturas_m12/C3.1.json) |
| `C3.2` | C3 — Menção inválida | `GET /module/Avaliacao/diarioApi` (`resource=nota&oper=post`) com nota `8.5` em regra sem nota | 200 (`any_error_msg: true`) | `modules.nota_componente_curricular` (`2 -> 2`, delta `0`) | SIM | [`C3.2.json`](../evidencias/g4_interacao_uso/capturas_m12/C3.2.json) |
| `C3.3` | C3 — Menção inválida | `GET /module/Avaliacao/diarioApi` (`resource=matriculas`) sem `matricula_id` nem `componente_curricular_id` | 200 (`any_error_msg: true`) | `modules.nota_aluno` (`10 -> 10`, delta `0`) | SIM | [`C3.3.json`](../evidencias/g4_interacao_uso/capturas_m12/C3.3.json) |
| `C4.1` | C4 — Conflito de matrícula | `POST /matricula/214/enturmar/137` em turma sem vagas remanescentes (`NoVacancyException`) | 302 (`-> 200` flash error) | `pmieducar.matricula_turma` (`35 -> 35`, delta `0`) | SIM | [`C4.1.json`](../evidencias/g4_interacao_uso/capturas_m12/C4.1.json) |
| `C4.2` | C4 — Conflito de matrícula | `POST /matricula/215/enturmar/138` com data `10/01/2026` anterior ao início acadêmico `01/02/2026` | 302 (`-> 200` flash error) | `pmieducar.matricula_turma` (`35 -> 35`, delta `0`) | SIM | [`C4.2.json`](../evidencias/g4_interacao_uso/capturas_m12/C4.2.json) |
| `C4.3` | C4 — Conflito de matrícula | `POST /matricula/216/enturmar/139` com outra enturmação ativa na matrícula `216` | 302 (`-> 200` flash error) | `pmieducar.matricula_turma` (`36 -> 36`, delta `0`) | SIM | [`C4.3.json`](../evidencias/g4_interacao_uso/capturas_m12/C4.3.json) |

*Fonte: `evidencias/g4_interacao_uso/capturas_m12/*.json`, `m12_ippe.csv` e `m12_ippe_execucao.log`. Todos os 12 cenários tiveram HTTP 500 = NÃO e persistência indevida = NÃO (`delta = 0`). Elaborado pelos autores.*

### 3.1 Veredito do Gate M12
Com 12 cenários bloqueados amigavelmente dentre os 12 executados (sem erro 500 nem persistência indevida no banco PostgreSQL):

$$
\text{IPPE} = \dfrac{12}{12} \times 100\% = 100{,}0\%
$$

O **Gate Binário M12 é formalmente APROVADO**. A hipótese de pesquisa **H4.1 é Confirmada**, comprovando em runtime que os validadores de entrada e exceções de domínio do i-Educar bloqueiam as 12 entradas inválidas previstas antes da escrita em banco.

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
| `C3.1` | *"O campo nota deve ser um número. (e mais 1 erro)"* | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: NÃO | Causa: SIM<br>Ação: NÃO | **Parcialmente autodescritiva** *(FormRequest v2: indica restrição numérica sem orientar uso de escala conceitual/tabela válida)* |
| `C3.2` | *"Nota não lançada, pois a regra de avaliação não utiliza nota."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C3.3` | *"É necessário receber matricula_id ou componente_curricular_id."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C4.1` | *"Não há vagas na turma \"6º Ano A (2026)\" #137."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C4.2` | *"A data de enturmação 10/01/2026 é anterior ao início do ano acadêmico 01/02/2026."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |
| `C4.3` | *"Existe outra enturmação ativa para a matrícula 216."* | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | Causa: SIM<br>Ação: SIM | **Totalmente autodescritiva** |

*Fonte: `evidencias/g4_interacao_uso/m13_admv.json` e `evidencias/g4_interacao_uso/capturas_m12/*.json` (vínculo `mensagem_sha256` validado). Elaborado pelos autores.*

### 4.2 Julgamento da Hipótese H4.2
- **Percentual de Autodescritividade:** Das 12 mensagens auditadas em execuções reais, **9 atendem cumulativamente aos requisitos de causa e ação corretiva** ($N_{\text{com causa e ação}} = 9$).
- Todas as 12 mensagens (100%) informam com clareza a causa do bloqueio.
- Três mensagens falham no critério de ação corretiva: `C2.2` e `C2.3` por constituírem mensagens secas do legado procedimental (`DiarioApiController.php`) sem informar a janela de datas autorizada nem orientar contato com a coordenação pedagógica, e `C3.1` (`PostNotasRequest` em `POST /api/v2/notas`), que informa apenas *"O campo nota deve ser um número. (e mais 1 erro)"* ao receber a menção textual `'ÓTIMO'`, sem explicitar qual escala/campo usar para avaliação conceitual nem detalhar o segundo erro no sumário.

$$
\text{ADMV} = \dfrac{9}{12} \times 100\% = 75{,}00\%
$$

O valor apurado de **$75{,}00\%$ enquadra-se no Nível Crítico ($S=1$)** por estar abaixo do limiar de $80{,}0\%$ estabelecido no Framework GQM. **A hipótese H4.2 é formalmente Refutada**, uma vez que o percentual medido ($75{,}00\%$) ficou aquém da faixa prevista ($[80{,}0\%, 90{,}0\%)$).

---

## 5. Impacto no Julgamento Final da Release E2 (Fase 5)

A aprovação do **Gate Binário M12 (IPPE = 100,0%)** é condição mandatória para que o software não seja reprovado automaticamente na Fase 5 da ISO/IEC 25040:2024:
- Se o Gate M12 houvesse falhado, o produto receberia imediatamente a **Classificação C (Reprovado / Bloqueado)** por falha em gate eliminatório.
- Com **M12 APROVADO (100,0%)**, o produto garante proteção transacional para os 12 cenários avaliados; entretanto, o enquadramento de **M13 em Nível Crítico ($S=1$, $\text{ADMV} = 75{,}00\%$)** impacta diretamente o critério da **Classe A** (que veda qualquer $S_i = 1$) e pressiona o índice agregado $\text{IQC}_{\text{Interação}}$, impondo ações corretivas prioritárias: (i) exibir as janelas de datas válidas nas recusas temporais de `DiarioApiController.php` (`C2.2`/`C2.3`) e (ii) detalhar mensagens orientadas à ação nos `FormRequest`s da API v2 (`PostNotasRequest`, `C3.1`).

---

## 6. Procedimento de Reprodução

Para reproduzir integralmente as checagens e relatórios a partir da raiz do repositório:

```bash
# 1. Conferir a integridade do catálogo congelado de cenários
(cd evidencias/g4_interacao_uso/m12_catalogo && shasum -a 256 -c manifesto.sha256)

# 2. Executar a suíte de testes unitários do avaliador
python3 -m unittest -v scripts/uso/test_avaliar_m12_m13.py

# 3. Executar o validador sobre o código-fonte do i-Educar e as 12 capturas HTTP/SQL brutas
python3 scripts/uso/avaliar_m12_m13.py \
  --path=./i-educar-src \
  --capturas-dir=evidencias/g4_interacao_uso/capturas_m12 \
  --output-dir=docs/evidencias/g4_interacao_uso

# 4. Validar aderência do site e links de documentação
bash scripts/docs/check_site.sh
```
