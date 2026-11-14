# Manutenibilidade: acoplamento, atrito legado e testes ativos (M8, M9 e M11)

Resultado da instrumentação e execução do motor estático da equipe (`scripts/evaluate-quality.php` v3.0.0) sobre o commit oficial congelado do **i-Educar 2.12**, em cumprimento à [Issue #44](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T02_GRACE_HOPPER/issues/44). As definições, fórmulas e faixas são as do [Framework GQM](../gqm_evaluation_framework.md) (M8, M9 e M11) e o roteiro operacional segue a Tabela 3 do [Plano de medição e testes](../plano_medicao_testes.md).

---

## 1. Execução e Integridade Metodológica

Em conformidade com os princípios de reproducibilidade da ISO/IEC 25040:2024 e do framework GQM, todos os três universos de medição foram formalizados e congelados em arquivos JSON com *digests* SHA-256 registrados em `evidencias/g3_manutenibilidade/manifestos/manifesto.sha256` antes da extração empírica.

**Tabela 1 — Dados da execução da coleta das métricas estruturais e de testes**

| Item | Valor |
| :--- | :--- |
| Produto | `portabilis/i-educar`, commit `7903a3efc7689942ee700007f86ed581023aad27` (branch `2.12`) |
| Instrumento | `scripts/evaluate-quality.php` versão 3.0.0 (`token_get_all` com resolução de `namespace` e `use` aliases para M8 + consumo de JUnit XML do runner Pest/PHPUnit para M11) |
| Data da coleta | 14/11/2026 |
| Comando de extração | `php scripts/evaluate-quality.php --path=./i-educar-src --evidence-dir=evidencias/g3_manutenibilidade` |
| Runner de testes (M11) | `vendor/bin/pest --colors=never --log-junit=/tmp/m11_runner_junit.xml` sobre os 30 arquivos do manifesto (PHP 8.5.11, Pest 5.3.2, PostgreSQL) |
| Manifestos congelados | `mapa_componentes_m8.json`, `manifesto_modelos_legacy_m9.json` e `manifesto_testes_m11.json` |
| Evidências geradas | [`m8_dspm.json`](../evidencias/g3_manutenibilidade/m8_dspm.json), [`m8_dspm.csv`](../evidencias/g3_manutenibilidade/m8_dspm.csv), [`m9_ifdl.json`](../evidencias/g3_manutenibilidade/m9_ifdl.json), [`m11_ttae.json`](../evidencias/g3_manutenibilidade/m11_ttae.json), [`m11_ttae.txt`](../evidencias/g3_manutenibilidade/m11_ttae.txt), [`m11_runner_junit.xml`](../evidencias/g3_manutenibilidade/m11_runner_junit.xml) e [`m11_runner.log`](../evidencias/g3_manutenibilidade/m11_runner.log) |

*Fonte: elaborado pelos autores.*

---

## 2. Resultados Consolidados

A Tabela 2 apresenta os valores consolidados obtidos para M8, M9 e M11, seus respectivos enquadramentos de nível ($S_i \in \{1, 2, 3, 4\}$) e a validação formal das hipóteses acadêmicas associadas.

**Tabela 2 — Valores medidos, nível de pontuação e julgamento de hipóteses (G3)**

| Métrica | Valor medido | Nível ($S_i$) | Hipótese associada | Resultado da hipótese |
| :--- | :---: | :---: | :--- | :--- |
| **M8** — $\text{DSPM}$ (Martin) | **0,3784** | Regular ($S=2$) | H3.2: $0{,}20 < \text{DSPM} \le 0{,}50$ | **Confirmada:** distância moderada decorrente de baixo uso de abstrações |
| **M9** — $\text{IFDL}$ (Fricção Legado) | **4,5556** | Crítico ($S=1$) | H3.3: $1{,}0 < \text{IFDL} \le 2{,}5$ | **Refutada:** densidade de adaptações foi superior à prevista ($4{,}56 > 2{,}5$) |
| **M11** — $\text{TTAE}$ (Testes Ativos) | **78,92%** | Regular ($S=2$) | H3.5: $70\% \le \text{TTAE} < 95\%$ | **Confirmada:** execução real do runner apontou 39 testes ignorados (`<skipped/>`) na suíte legada (`146/185` ativos com asserção) |

*Fonte: elaborado pelos autores a partir da execução do motor estático e do runner Pest/PHPUnit no commit `7903a3e`.*

---

## 3. M8 — Distância da Sequência Principal de Martin (DSPM)

A métrica M8 avalia o balanço arquitetural entre abstração e acoplamento nos componentes dos domínios de Matrícula e Notas/Diário. O universo congelado engloba 5 componentes atômicos, totalizando 47 classes/tipos concretos e abstratos e 42 pares distintos de dependência entre componentes (`srcFqn -> dstFqn`), resolvidos considerando `namespace` e aliases `use`.

$$
I = \dfrac{C_e}{C_a + C_e}, \qquad A = \dfrac{N_a}{N_c}, \qquad D = |A + I - 1|, \qquad \text{DSPM} = \dfrac{1}{P}\sum_{p=1}^{P} D_p
$$

**Tabela 3 — Acoplamento, abstração e distância por componente analisado**

| Componente | $N_c$ | $N_a$ | Abstração ($A$) | $C_a$ | $C_e$ | Instabilidade ($I$) | Distância ($D$) | Diagnóstico de Design |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `C1_Matricula_Services` | 3 | 0 | 0,000 | 3 | 4 | 0,571 | 0,429 | Balanceado com leve viés de dependência de saída sobre modelos/legado |
| `C2_Matricula_Controllers` | 3 | 0 | 0,000 | 0 | 3 | 1,000 | 0,000 | Totalmente instável ($I=1$), alinhado à Sequência Principal |
| `C3_Dominio_Models` | 11 | 0 | 0,000 | 8 | 0 | 0,000 | 1,000 | Zona de Dor: altamente estável ($C_a=8$), porém sem abstrações ($A=0$) |
| `C4_Avaliacao_Service_Legado` | 22 | 3 | 0,136 | 6 | 4 | 0,400 | 0,464 | Monólito legado com baixa abstração e acoplamento misto |
| `C5_Avaliacao_Views_Api_Legado` | 8 | 0 | 0,000 | 0 | 12 | 1,000 | 0,000 | Totalmente instável como camada cliente/exposição (`I=1`), na Sequência Principal |
| **MÉDIA GLOBAL ($\text{DSPM}$)** | **47** | **3** | — | — | — | — | **0,3784** | **Nível Regular ($S=2$, faixa $(0{,}35, 0{,}50]$)** |

*Fonte: `evidencias/g3_manutenibilidade/m8_dspm.csv` e `m8_dspm.json`. Elaborado pelos autores.*

### 3.1 Análise Arquitetural do Acoplamento
- O componente `C3_Dominio_Models` apresenta o ponto crítico de acoplamento da arquitetura: com 11 modelos consumidos por serviços e controladores legados e modernos ($C_a=8, C_e=0 \implies I=0$), a ausência completa de interfaces ($A=0$) projeta o componente diretamente para a **Zona de Dor (*Zone of Pain*)**, resultando em distância máxima $D = |0 + 0 - 1| = 1{,}000$.
- Os componentes `C2_Matricula_Controllers` ($C_a=0, C_e=3 \implies I=1$) e `C5_Avaliacao_Views_Api_Legado` ($C_a=0, C_e=12 \implies I=1$) situam-se no extremo oposto: atuam puramente como camadas consumidoras/de exposição, atingindo equilíbrio exato na Sequência Principal ($D = |0 + 1 - 1| = 0{,}000$).
- A média aritmética $\text{DSPM} = 0{,}3784$ confirma a hipótese `H3.2`, refletindo uma arquitetura típica de monólitos em transição em que o domínio de dados é concreto e rígido.

---

## 4. M9 — Índice de Fricção de Dados Legado-Moderno (IFDL)

A métrica M9 mensura o esforço e a sobrecarga de adaptação defensiva de dados entre o núcleo procedural legado (`pmieducar`/`modules`) e a camada moderna Laravel Eloquent (`app/Models/Legacy*.php`).

O universo congelado abrange os 18 modelos `Legacy*.php` utilizados nos fluxos de Matrícula e Avaliação. Foram catalogadas **82 adaptações defensivas** distribuídas em três categorias da rubrica:
1. `LEGADO_SCHEMA_MAP`: Qualificação explícita de esquema PostgreSQL legado (`pmieducar.*`, `modules.*`), mapeamento de chaves primárias legadas (`cod_*`) e array `$legacy`.
2. `TYPE_CAST_NULL_FILTER`: Conversões explícitas em `$casts` e mutators/accessors de tipo (`Attribute::make`).
3. `QUERY_SCOPE_ADAPTER`: Escopos de consulta e filtros defensivos de status.

$$
\text{IFDL} = \dfrac{1}{M_{\text{modelos}}}\sum_{i=1}^{M_{\text{modelos}}} A_{\text{defensivos}, i} = \dfrac{82}{18} = 4{,}5556 \text{ adaptações/modelo}
$$

**Tabela 4 — Inventário de adaptações defensivas nos modelos Legacy em escopo**

| Modelo Analisado | Tabela PostgreSQL Mapeada | Chave Primária | Adaptadores Mapeados | Categoria Predominante |
| :--- | :--- | :--- | :---: | :--- |
| `LegacySchoolClass` | `pmieducar.turma` | `cod_turma` | **18** | Schema map e accessors de atributos |
| `LegacyRegistration` | `pmieducar.matricula` | `cod_matricula` | **14** | Casts de datas, schema map e accessors |
| `LegacyStudent` | `pmieducar.aluno` | `cod_aluno` | **11** | Chaves legadas e casts |
| `LegacyDiscipline` | `modules.componente_curricular` | `id` | **9** | Schema map e accessors |
| `LegacyEnrollment` | `pmieducar.matricula_turma` | `id` | **8** | Casts e array `$legacy` |
| `LegacyEvaluationRule` | `modules.regra_avaliacao` | `id` | **4** | Schema map e relacionamentos |
| `LegacyValueRoundingTable` | `modules.tabela_arredondamento_valor` | `id` | **2** | Schema map e casts |
| `LegacyScoreExam` | `modules.nota_exame` | `id` | **2** | Schema map e casts |
| `LegacyAcademicYearStage` | `pmieducar.ano_letivo_modulo` | `id` | **2** | Schema map e casts |
| `LegacyRemedialRule` | `modules.regra_recuperacao` | `id` | **2** | Schema map |
| `LegacyAverageFormula` | `modules.formula_media` | `id` | **2** | Schema map |
| `LegacyDisciplineScoreAverage` | `modules.nota_componente_curricular_media` | `id` | **2** | Schema map |
| `LegacyRoundingTable` | `modules.tabela_arredondamento` | `id` | **1** | Schema map |
| `LegacyDisciplineScore` | `modules.nota_componente_curricular` | `id` | **1** | Schema map |
| `LegacyStudentScore` | `modules.nota_aluno` | `id` | **1** | Schema map |
| `LegacyRegistrationScore` | `modules.nota_aluno` | `id` | **1** | Schema map |
| `LegacyStudentAbsence` | `modules.falta_aluno` | `id` | **1** | Schema map |
| `LegacySchoolYearLock` | `pmieducar.bloqueio_ano_letivo` | `id` | **1** | Schema map |
| **TOTAL CONSOLIDADO** | **18 modelos de domínio** | — | **82 adaptadores** | **$\text{IFDL} = 4{,}56$ (Nível Crítico, $S=1$)** |

*Fonte: `evidencias/g3_manutenibilidade/m9_ifdl.json`. Elaborado pelos autores.*

### 4.1 Julgamento da Hipótese H3.3
A hipótese `H3.3` estimava que os modelos apresentariam em média entre 1,0 e 2,5 adaptações defensivas por modelo. O valor empírico apurado ($\text{IFDL} = 4{,}56$) **refuta a hipótese H3.3**, revelando que a camada de persistência exige mais do que o dobro de tratamento defensivo do que o suposto previamente. Os modelos centrais de Matrícula (`LegacyRegistration`, 14 adaptadores) e Turma (`LegacySchoolClass`, 18 adaptadores) concentram 39% de todas as adaptações do sistema, demonstrando alta fricção na convivência entre os esquemas legados e o framework moderno.

---

## 5. M11 — Taxa de Testes Ativos com Asserção em Domínio (TTAE)

A métrica M11 avalia a efetividade e a integridade da suíte de testes automatizados nos domínios de Matrícula e Notas/Diário por meio da execução real do runner (`vendor/bin/pest --colors=never --log-junit`), registrando o status de cada caso e a contagem de asserções executadas em runtime. Casos ignorados (`<skipped/>`), casos ativos com zero asserções ou casos com falha/erro não entram no numerador.

O manifesto congelado mapeia **30 arquivos de teste**, nos quais o runner descobriu e reportou **185 casos no relatório JUnit**, com **1038 asserções totais** (**938** em casos ativos não ignorados), **0 falhas/erros** e **0 casos ativos sem asserção**.

$$
\text{TTAE} = \dfrac{N_{\text{ativos com asserção}}}{N_{\text{casos descobertos pelo runner}}} \times 100\% = \dfrac{146}{185} \times 100\% = 78{,}92\%
$$

**Tabela 5 — Distribuição de testes descobertos, ignorados (`<skipped/>`) e ativos com asserção por diretório**

| Subdiretório de Teste | Arquivos | Casos no Runner | `<skipped/>` | Ativos c/ 0 Asserções | Ativos c/ Asserção | Asserções (Ativos) | Taxa Ativa Local |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `tests/Unit/Modules/Service` (Legado) | 19 | 77 | 39 | 0 | 38 | 587 | **49,35%** |
| `tests/Unit/Exceptions` (Domínio) | 4 | 4 | 0 | 0 | 4 | 5 | 100,00% |
| `tests/Unit/Enum` | 1 | 3 | 0 | 0 | 3 | 8 | 100,00% |
| `tests/Feature/Services` (Laravel) | 1 | 27 | 0 | 0 | 27 | 77 | 100,00% |
| `tests/Feature/Commands` | 1 | 2 | 0 | 0 | 2 | 5 | 100,00% |
| `tests/Feature/Api/V2` (REST) | 3 | 71 | 0 | 0 | 71 | 249 | 100,00% |
| `tests/Api` | 1 | 1 | 0 | 0 | 1 | 7 | 100,00% |
| **TOTAL CONSOLIDADO** | **30** | **185** | **39** | **0** | **146** | **938** | **$\text{TTAE} = 78{,}92\%$ (Regular, $S=2$)** |

*Fonte: `evidencias/g3_manutenibilidade/m11_runner_junit.xml`, `m11_runner.log`, `m11_ttae.json` e `m11_ttae.txt`. Elaborado pelos autores.*

### 5.1 Julgamento da Hipótese H3.5
- A hipótese `H3.5` previa que a presença de `markTestSkipped()` na suíte legada situaria a taxa ativa entre 70% e 95%. Com $\text{TTAE} = 78{,}92\%$, **a hipótese H3.5 é confirmada**.
- As suítes modernas (`tests/Feature/`, `tests/Unit/Exceptions/`, `tests/Unit/Enum/` e `tests/Api/`) apresentam **100% de atividade com asserção** (`108` de `108` casos ativos).
- Em contrapartida, na suíte legada de `tests/Unit/Modules/Service/`, **50,65% dos casos executados pelo runner (39 de 77)** terminaram em `<skipped/>` (abrangendo `FaltaComponenteSituacaoTest`, `FaltaComponenteTest`, `FaltaGeralSituacaoTest`, `FaltaGeralTest`, `InicializacaoTest`, `NotaConceitualSituacaoTest`, `NotaNumericaSituacaoTest`, `NotaRecuperacaoTest`, `NotaTest`, `ParecerDescritivo*Test` e `UtilityTest`). Note-se que 6 casos que executaram asserções parciais (100 asserções no total) antes de invocar `markTestSkipped()` foram corretamente excluídos do numerador por constarem com status `skipped`.

---

## 6. Procedimento de Reprodução

Para reproduzir integralmente as medições a partir da raiz do repositório:

```bash
# 1. Conferir integridade dos manifestos congelados
(cd evidencias/g3_manutenibilidade/manifestos && shasum -a 256 -c manifesto.sha256)

# 2. Executar suíte de testes unitários do motor de avaliação estática (39 verificações)
php scripts/tests/evaluate_quality_test.php

# 3. Executar motor de extração sobre o checkout oficial do i-Educar com o JUnit capturado pelo Pest
php scripts/evaluate-quality.php \
  --path=./i-educar-src \
  --m11-junit=evidencias/g3_manutenibilidade/m11_runner_junit.xml \
  --evidence-dir=evidencias/g3_manutenibilidade

# 4. Validar aderência do site e links da documentação
bash scripts/docs/check_site.sh
```
