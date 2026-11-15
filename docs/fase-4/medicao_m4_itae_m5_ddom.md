# Medição M4 (ITAE) e M5 (DDOM) — Atomicidade Transacional e Triagem

**Issue:** #23
**Milestone:** M5 (Instrumentação e Execução das Medições — Fase 4 ISO/IEC 25040:2024)
**Fase ISO/IEC 25040:2024:** 4 (Execução da Avaliação)
**Característica ISO/IEC 25010:2023:** Confiabilidade (Tolerância a Falhas / Recuperabilidade)
**Commit do produto:** `7903a3efc7689942ee700007f86ed581023aad27` (branch `2.12`, `portabilis/i-educar`)
**Ambiente:** `scripts/avaliacao/m3/compose.yml` — PHP 8.5.12, PostgreSQL 18.7, Redis 8.10.3
**Rodada:** `rodada-001` (diagnostic)
**Data:** 2026-11-15
**Resultado:** [preencher na Etapa D]

## 1. Objetivo e métrica
### 1.1 ITAE (M4 — Gate binário)
### 1.2 DDOM (M5 — Triagem)
### 1.3 Hipóteses (H2.2)

## 2. Inventário congelado de operações compostas
[referenciar docs/plano_medicao_testes.md §4.x — NÃO duplicar]

## 3. Metodologia de injeção de falhas

## 4. Resultados por operação
### 4.1 OP-01 — Boletim::save()
### 4.2 OP-02 — updateStatus (se aplicável)
### 4.3 OP-03 — cancelRegistration (referência positiva)
### 4.4 OP-04 — updateMediaComponente/Geral (se aplicável)

## 5. Cálculo do ITAE e veredito do Gate M4

## 6. Triagem M5 (DDOM) e regra de tratamento

## 7. Limitações e impedimentos

## 8. Rastreabilidade (commits, hashes, evidências)

## 9. Referências (ISO/IEC 25010:2023, 25040:2024, GQM v2.0, plano)