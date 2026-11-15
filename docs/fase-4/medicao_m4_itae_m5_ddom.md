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

Ver §8.1 do [Plano Operacional de Medição e Testes](../plano_medicao_testes.md#81-inventário-congelado-de-operações-compostas). Quatro operações identificadas: OP-01 (`Boletim::save()`), OP-02 (`RegistrationService::updateStatus()`, bloqueada por `transferencia_tipo`/`situacao_matricula` vazias), OP-03 (`cancelRegistration()`, referência positiva com `DB::transaction`), OP-04 (`updateMediaComponente/Geral()`).

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

**Estado final (BEFORE = 0 em todas; AFTER após falha):**

| Tabela | BEFORE | AFTER | Δ | Origem |
| :--- | :-: | :-: | :-: | :--- |
| `modules.nota_aluno` | 0 | 1 | **+1** | `saveNotas()` comitada |
| `modules.nota_componente_curricular` | 0 | 1 | **+1** | `saveNotas()` comitada |
| `modules.falta_aluno` | 0 | 1 | +1 | construtor (`_loadFalta`), não `saveFaltas()` |
| `modules.falta_componente_curricular` | 0 | 0 | 0 | `saveFaltas()` nunca executou |
| `pmieducar.matricula.aprovado` | 3 | 3 | 0 | `promover()` nunca executou |

**Evidência SQL de órfão estrutural** (`op01-orphans.log`):

**Classificação:** NÃO ATÔMICA. `ITAE_OP-01 = 0%` (1 execução, 0 atômicas).

**Observação metodológica.** O `falta_aluno=1` **não** é resultado de `saveFaltas()` ter rodado parcialmente — o método não foi invocado (a injeção dispara antes). A linha foi criada pelo construtor, via `_loadFalta()` (`Boletim.php:378`), como container de faltas. Se o experimento fosse conduzido com snapshot **após instanciação**, `falta_aluno=1` já estaria no "BEFORE" e a evidência de não-atomicidade seria idêntica: `nota_aluno` comita, `falta_componente_curricular` não. A inconsistência é a mesma — o estado pós-falha não reverte ao estado pré-`save()`.

**Ameaça à validade.** O experimento isola a falha entre as duas primeiras escritas. A injeção entre `saveFaltas()` e `savePareceres()`, ou entre `savePareceres()` e `promover()`, não foi executada. A classificação "não atômica" decorre de uma única injeção, suficiente para provar que o método não é atômico em geral (basta uma falha intermediária não revertida). Execuções adicionais em outros pontos enriqueceriam a caracterização, mas não mudariam o veredito binário.

## 5. Cálculo do ITAE e veredito do Gate M4

[Preencher na Etapa D.]

## 6. Triagem M5 (DDOM) e regra de tratamento

[Preencher na Etapa D.]

## 7. Rastreabilidade

| Item | Valor |
| :--- | :--- |
| Commit do produto | `7903a3efc7689942ee700007f86ed581023aad27` |
| Worktree clean (antes do harness) | `true` |
| Hash do `compose.yml` | `9770b6d0b24a6c5bcca57ac4fc3696040e1f2c2670ea26335ff1581cb6c38fc5` |
| Hash do `Dockerfile` do produto | `edfb3b4bbf237648eaa7e56e9d08f37b24faa33df2709b32ac98e14c4e12c166` |
| Hash do baseline | `1d1510c6cae5b79c2e641dfa87d45f1323e25f696314dafa6d6106bd4c0e3ac7` |
| Seed | `DemoSeeder` — 210 alunos, 210 matrículas (ano 2026) |