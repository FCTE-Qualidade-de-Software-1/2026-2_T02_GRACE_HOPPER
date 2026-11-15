# Medição M4 (ITAE) e M5 (DDOM) — Atomicidade Transacional e Triagem

**Issue:** #23
**Milestone:** M5
**Fase ISO/IEC 25040:2024:** 4
**Característica ISO/IEC 25010:2023:** Confiabilidade (Tolerância a Falhas)
**Commit do produto:** `7903a3efc7689942ee700007f86ed581023aad27`
**Ambiente:** `scripts/avaliacao/m3/compose.yml` — PHP 8.5.12, PostgreSQL 18.7, Redis 8.10.3
**Rodada:** `rodada-001` (`run_type: diagnostic`)
**Data da coleta do caminho feliz:** 2026-11-15

## 1. Objetivo e métrica

### 1.1 ITAE (M4 — Gate binário)

O Índice de Transações Atômicas Efetivas mede o percentual de operações multi-escrita que revertem integralmente quando uma falha é injetada em etapa intermediária:

$$
\text{ITAE} = \frac{N_{\text{atômicas}}}{N_{\text{testadas}}} \times 100\%
$$

Gate binário: ITAE = 100% → aprovado; ITAE < 100% → bloqueado (Classe C por §3.3 do Plano).

### 1.2 DDOM (M5 — Triagem)

M5 (Densidade de Defeitos Operacionais Médios) depende de telemetria de produção. A triagem de mensurabilidade segue o checklist da §3.1 do Plano, com política de renormalização pré-declarada: se não mensurável, o peso $w_{\text{M5}} = 1{,}2$ é excluído do $\text{IQC}_{\text{Confiabilidade}}$.

### 1.3 Hipóteses

**H2.2:** o fluxo legado do i-Educar não é 100% atômico → ITAE < 100%.

## 2. Inventário congelado

Ver §8.1 do [Plano Operacional de Medição e Testes](../plano_medicao_testes.md). Quatro operações identificadas: OP-01 (`Boletim::save()`), OP-02 (`RegistrationService::updateStatus()`, bloqueada por `transferencia_tipo`/`situacao_matricula` vazias), OP-03 (`cancelRegistration()`, referência positiva com `DB::transaction`), OP-04 (`updateMediaComponente/Geral()`).

## 3. Metodologia e caminho feliz

### 3.1 Método de execução

Harness PHP executado via `php artisan tinker --execute` no container `php` do ambiente, sem alteração de código-fonte do produto. O script (`evidencias/g2_confiabilidade/m4/rodada-001/happy_path_op01.php`) instancia `Avaliacao_Service_Boletim(['matricula' => 3])`, adiciona uma nota (`Avaliacao_Model_NotaComponente`, componente 8, etapa '1', nota 8.5) e uma falta (`Avaliacao_Model_FaltaComponente`, componente 8, etapa '1', quantidade 2), e invoca `save()`.

A escolha do componente 8 decorre do fallback `IedFinder::getComponentesTurma` (`ieducar/lib/App/Model/IedFinder.php:562`): como `modules.componente_curricular_turma` está vazia para a turma 3, o método delega a `getEscolaSerieDisciplina(serie 6, escola 2)` e retorna 9 componentes (IDs 8–16). Nenhuma fixture adicional foi necessária (ver IMP-05).

O `etapaAtual` do serviço retorna `NULL` e `etapas` retorna `4`; o harness usa `etapa = '1'` explicitamente em `addNota`/`addFalta`.

### 3.2 Resultado do caminho feliz

Execução bem-sucedida das três primeiras escritas do `save()`, com a quarta (`promover()`) lançando `CoreExt_Service_Exception` de alerta:

Estado após a execução:

| Tabela | Linhas após | Detalhe |
| :--- | :-: | :--- |
| `modules.nota_aluno` | 1 | `id=3`, `matricula_id=3` |
| `modules.nota_componente_curricular` | 1 | `nota_aluno_id=3`, `componente_curricular_id=8`, `etapa='1'`, `nota=8.5000` |
| `modules.falta_aluno` | 1 | `id=3`, `matricula_id=3` |
| `modules.falta_componente_curricular` | 1 | `falta_aluno_id=3`, `componente_curricular_id=8`, `etapa='1'`, `quantidade=2` |
| `pmieducar.matricula` (3) | `aprovado=3` | inalterado |

Evidência bruta em `op01-before.log`, `op01-happy.log`, `op01-after.log`, `op01-after-detail.log`.

### 3.3 Ameaças à validade

1. **`promover()` lança exceção de alerta** quando a situação calculada coincide com a anterior. Em produção, `trySaveServiceBoletim` (`DiarioApiController.php:1097`) engole `CoreExt_Service_Exception`, então o usuário não vê erro e as escritas anteriores permanecem comitadas. Registrado como IMP-07.
2. **Warnings DEPRECATED** de `pg_escape_string` e `trim(null)` poluem stdout com PHP 8.5 (IMP-06). Não gravam nada; foram preservados nos logs com `2>&1`.
3. **IDs iniciaram em 3** (não 1) por resíduos de tentativas anteriores; as sequences foram resetadas via `TRUNCATE ... RESTART IDENTITY CASCADE` antes da Etapa C.
4. **Amostra única:** apenas a matrícula 3 foi usada no caminho feliz. A generalização para as 210 matrículas do `DemoSeeder` não é inferida.

## 4. Injeção determinística e verificação de órfãos

### 4.1 OP-01 — Boletim::save() — NÃO ATÔMICO

**Método de injeção.** `RuntimeException` inserida entre `$this->saveNotas()` e `$this->saveFaltas()` em `Boletim.php` (linha 2600 após patch), controlada pela variável `M4_FAULT_INJECT_OP01=1`. Patch versionado em `patches/OP-01.patch`; aplicado via `sed`, revertido com `cp` do original. Determinismo: a variável de ambiente decide se a falha ocorre.

**Cronologia observada.**

1. `new Avaliacao_Service_Boletim(['matricula' => 3])` → construtor chama `_loadFalta()` (`Boletim.php:378`), que cria `falta_aluno.id=1` (container sem itens) via `_createFaltaAluno()`.
2. `addNota(...)` e `addFalta(...)` apenas populam estruturas em memória.
3. `save()` → `saveNotas()` comita `nota_aluno.id=1` e `nota_componente_curricular.id=1` (componente 8, etapa '1', nota 8.5).
4. **Injeção dispara** entre `saveNotas()` e `saveFaltas()` → `RuntimeException: FAULT_INJECTION_OP01_BETWEEN_SAVE_NOTAS_AND_FALTAS` (exit code ≠ 0).
5. `saveFaltas()`, `savePareceres()` e `promover()` não executam.

**Nota sobre IDs.** A Etapa B registrou `nota_aluno.id=3` (resíduo de tentativas anteriores). Antes da Etapa C, as sequences foram resetadas via `TRUNCATE ... RESTART IDENTITY CASCADE`, e a injeção gerou `id=1`. A diferença é cosmética — o estado (0 → 1) e a classificação (não atômico) não mudam.

**Estado final (BEFORE = 0 em todas; AFTER após falha):**

| Tabela | BEFORE | AFTER | Δ | Origem |
| :--- | :-: | :-: | :-: | :--- |
| `modules.nota_aluno` | 0 | 1 | **+1** | `saveNotas()` comitada |
| `modules.nota_componente_curricular` | 0 | 1 | **+1** | `saveNotas()` comitada |
| `modules.falta_aluno` | 0 | 1 | +1 | construtor (`_loadFalta`), não `saveFaltas()` |
| `modules.falta_componente_curricular` | 0 | 0 | 0 | `saveFaltas()` nunca executou |
| `pmieducar.matricula.aprovado` | 3 | 3 | 0 | `promover()` nunca executou |

**Evidência SQL de órfão estrutural** (`op01-orphans.log`):

```text
 check_name     | nota_aluno_id | nota_comp | nota_etapa |  nota  | falta_aluno_id | falta_comp_id |              classificacao
----------------+---------------+-----------+------------+--------+----------------+---------------+-----------------------------------------
 OP01_estado_final |             1 |         8 | 1          | 8.5000 |              1 |               | ORFAO: falta_aluno sem falta_componente

   check_name    | nota_aluno | nota_comp | falta_aluno | falta_comp
-----------------+------------+-----------+-------------+------------
 contagens_final |          1 |         1 |           1 |          0
```

**Classificação:** NÃO ATÔMICA. `ITAE_OP-01 = 0%` (1 execução, 0 atômicas).

**Observação metodológica.** O `falta_aluno=1` **não** é resultado de `saveFaltas()` ter rodado parcialmente — o método não foi invocado (a injeção dispara antes). A linha foi criada pelo construtor, via `_loadFalta()` (`Boletim.php:378`), como container de faltas. Se o experimento fosse conduzido com snapshot **após instanciação**, `falta_aluno=1` já estaria no "BEFORE" e a evidência de não-atomicidade seria idêntica: `nota_aluno` comita, `falta_componente_curricular` não. A inconsistência é a mesma — o estado pós-falha não reverte ao estado pré-`save()`.

**Ameaça à validade.** O experimento isola a falha entre as duas primeiras escritas. A injeção entre `saveFaltas()` e `savePareceres()`, ou entre `savePareceres()` e `promover()`, não foi executada. A classificação "não atômica" decorre de uma única injeção, suficiente para provar que o método não é atômico em geral (basta uma falha intermediária não revertida). Execuções adicionais em outros pontos enriqueceriam a caracterização, mas não mudariam o veredito binário.

## 5. Cálculo do ITAE e veredito do Gate M4

### 5.1 Cálculo

$$
\text{ITAE} = \frac{N_{\text{atômicas}}}{N_{\text{testadas}}} \times 100\% = \frac{0}{1} \times 100\% = 0{,}0\%
$$

**Denominador (n = 1):** OP-01 apenas. OP-02 e OP-03 não integram o denominador nesta rodada:
- OP-02 (`updateStatus` TRANSFERIDO) está bloqueada por `pmieducar.transferencia_tipo` e `relatorio.situacao_matricula` vazias no `DemoSeeder`;
- OP-03 (`cancelRegistration`) é referência positiva (tem `DB::transaction`) mas não foi executada nesta coleta;
- OP-04 (`updateMediaComponente/Geral`) é recorte secundário do `Boletim`, funcionalmente coberto por OP-01.

### 5.2 Veredito do Gate M4

**Gate M4 = FAIL** (ITAE = 0% < 100%). A operação testada (OP-01) não reverte integralmente sob falha intermediária: `nota_aluno` e `nota_componente_curricular` permanecem comitadas enquanto `falta_componente_curricular` não é gravada. **H2.2 confirmada no recorte OP-01.**

**Consequência para a release (por §3.3 do Plano):** Classe C (Reprovado / Bloqueado). Falha em gate binário determina Classe C independentemente do $\text{IQM}$ global. O $\text{IQM}$ não é calculado nesta issue; o resultado de M4 entra como insumo negativo no julgamento da Fase 5.

### 5.3 Limitações do denominador

A amostra é mínima (n = 1). A generalização para o universo de operações multi-escrita do i-Educar exige:
- popular `transferencia_tipo` e `situacao_matricula` para desbloquear OP-02;
- executar OP-03 como referência positiva (aumenta a credibilidade do instrumento ao demonstrar que ele **detecta** atomicidade quando presente);
- executar OP-04 como recorte adicional do `Boletim`.

Essas execuções enriqueceriam a caracterização, mas não alterariam o veredito binário: basta uma falha intermediária não revertida para reprovar o método no critério do Gate M4.

## 6. Triagem M5 (DDOM) e regra de tratamento

### 6.1 Checklist de mensurabilidade

| # | Pergunta de instrumentação | Verificação empírica | Resultado |
| :-: | :--- | :--- | :-: |
| D1 | Há logs de transação acessíveis? | `grep -rn "Log::\|Monolog\|error_log"` em `app/` e `ieducar/modules/Avaliacao/` retornou 3 ocorrências: 1 ativa em `SchoolGradeBatchUpdateController.php:84` (contexto de batch import) e 2 comentadas em `DiarioApiController.php:1103` e `PromocaoApiController.php:108`. Nenhuma registra transação de matrícula/notas. | Não |
| D2 | Existem tabelas de auditoria/eventos? | 4 tabelas: `modules.auditoria`, `public.ieducar_audit`, `public.log_unification_old_data`, `public.log_unifications`. As três últimas são de **unificação de dados** (migração histórica), não de eventos de negócio. `modules.auditoria` existe mas não registra operações de matrícula/notas em runtime. | Parcial |
| D3 | Há identificador de rollback no núcleo legado? | `grep -n "rollback\|ROLLBACK\|savepoint"` em `ieducar/lib/CoreExt/DataMapper.php` retornou vazio. O mapper legado não tem controle transacional próprio. | Não |
| D4 | Há métrica de confiabilidade exposta? | `grep -rn "metrics\|/health\|/status"` em `routes/` e `app/Http/` retornou 3 endpoints, todos de `/status` de **importação em lote** (`final-status-import`, `academic-year`, `school-grade.batch-update`), não de confiabilidade ou saúde de transações. | Não |
| D5 | É possível reconstruir taxa de sucesso/falha por SQL? | `modules.auditoria` existe (confirmado via `\dt`), mas não há registros de transação de matrícula/notas em runtime. A tabela está vazia de eventos relevantes ao recorte avaliado. | Não |

**Síntese:** 0 critérios plenamente atendidos, 1 parcial (D2). Total abaixo do limiar de 4/5 do plano para mensurabilidade.

### 6.2 Condição de M5

**M5 (DDOM) = NÃO MENSURÁVEL** no recorte avaliado. Justificativa:

1. O núcleo legado não registra transações de negócio em log estruturado — as mensagens existentes são de contexto de batch import ou estão comentadas.
2. As tabelas de auditoria disponíveis (`ieducar_audit`, `log_unification*`) referem-se a operações de migração histórica, não a operações de matrícula/notas em runtime.
3. Não há identificador de rollback nem savepoint no `CoreExt/DataMapper` legado que permita rastrear reversão por transação.
4. Não há métrica operacional de confiabilidade exposta por endpoint, dashboard ou SQL reconstrutível.

Essa condição **confirma a previsão da Hipótese H2.2** quanto à não mensurabilidade de M5 no fluxo legado.

### 6.3 Aplicação da política pré-declarada (§3.1 do Plano)

Conforme a política de renormalização pré-declarada em §3.1 do Plano Operacional, o peso original $w_{\text{M5}} = 1{,}2$ é **excluído do denominador** da característica Confiabilidade. O $\text{IQC}_{\text{Confiabilidade}}$ passa a ser computado apenas com as métricas que possuem dados comprovados:

$$
\text{IQC}_{\text{Confiabilidade}} = \frac{S_{\text{M3}} \times 2{,}0 + S_{\text{M4}} \times 2{,}0 + S_{\text{M6}} \times 1{,}0}{2{,}0 + 2{,}0 + 1{,}0}
$$

Com os resultados desta rodada:
- $S_{\text{M3}} = 4$ (DCNM = 100%, Gate M3 aprovado em `oficial-001`, conforme [Medição M3](medicao_m3_dcnm.md));
- $S_{\text{M4}} = 1$ (ITAE = 0%, Gate M4 FAIL);
- $S_{\text{M6}}$ depende da execução de M6 (backup/restore) e não é calculado nesta issue.

A exclusão de M5 evita atribuição de nota substituta arbitrária e preserva a integridade do índice. A limitação é registrada no artigo e no presente relatório (§7), com a previsão de coleta futura em ambiente com telemetria operacional.

## 7. Rastreabilidade

| Item | Valor |
| :--- | :--- |
| Commit do produto | `7903a3efc7689942ee700007f86ed581023aad27` |
| Worktree clean (antes do harness) | `true` |
| Hash do `compose.yml` | `9770b6d0b24a6c5bcca57ac4fc3696040e1f2c2670ea26335ff1581cb6c38fc5` |
| Hash do `Dockerfile` do produto | `edfb3b4bbf237648eaa7e56e9d08f37b24faa33df2709b32ac98e14c4e12c166` |
| Hash do baseline | `1d1510c6cae5b79c2e641dfa87d45f1323e25f696314dafa6d6106bd4c0e3ac7` |
| Seed | `DemoSeeder` — 210 alunos, 210 matrículas (ano 2026) |