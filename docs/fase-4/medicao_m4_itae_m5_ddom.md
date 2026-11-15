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
