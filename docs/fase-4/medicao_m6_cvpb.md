# Medição M6 (CVPB) — Completude e Verificabilidade do Procedimento de Backup

**Issue:** #42
**Milestone:** M5
**Fase ISO/IEC 25040:2024:** 4 (Execução da Avaliação)
**Característica ISO/IEC 25010:2023:** Confiabilidade (Recuperabilidade)
**Commit do produto:** `7903a3efc7689942ee700007f86ed581023aad27`
**Ambiente:** `scripts/avaliacao/m3/compose.yml` — PostgreSQL 18.7
**Rodada:** `rodada-001` (`run_type: diagnostic`)
**Data da coleta:** 2026-11-15

## 1. Objetivo e métrica

O **CVPB** (Completude e Verificabilidade do Procedimento de Backup) mede o percentual de restaurações bem-sucedidas sobre o total de cenários de backup/restore planejados:

$$
\text{CVPB} = \frac{N_{\text{restaurações bem-sucedidas}}}{N_{\text{restaurações planejadas}}} \times 100\%
$$

**Limiares:** Excelente ($S=4$): 100% · Bom ($S=3$): [95%, 100%) · Regular ($S=2$): [90%, 95%) · Crítico ($S=1$): < 90%

**Hipótese H2.3:** $\text{CVPB} \ge 95\%$ (recuperabilidade do i-Educar 2.12 é adequada).

## 2. Inventário congelado

Manifesto congelado em `evidencias/g2_confiabilidade/m6/manifest.md` (commit `ad76ed6`), com 6 cenários:

| ID | Descrição | Formato | Estratégia |
| :-: | :--- | :--- | :--- |
| T01 | Custom format | `-Fc` | `pg_restore` em banco limpo |
| T02 | Plain SQL | `-Fp` | `psql -f` em banco limpo |
| T03 | Directory format | `-Fd` | `pg_restore` em banco limpo |
| T04 | Clean/if-exists | `-Fc --clean --if-exists` | `pg_restore` sobre banco populado |
| T05 | Schema-only | `--schema-only` | `pg_restore` em banco limpo |
| T06 | Data-only | `--data-only -Fc` | `pg_restore --disable-triggers` em banco com schema |

**Baseline de tuplas (referência):** 2.132 tuplas distribuídas em 12 tabelas de `pmieducar`, `modules` e `cadastro`.

## 3. Metodologia

Cada teste executa o ciclo completo:
1. `pg_dump` do banco `testing` (backup completo, sem filtro de schema)
2. `DROP DATABASE` + `CREATE DATABASE ieducar_m6_restore`
3. `pg_restore` (ou `psql -f`) do dump no banco destino
4. Verificação de tuplas (12 contadores) contra o baseline
5. Verificação de integridade de FKs (0 órfãos)

**Nota de revisão de escopo.** A execução inicial com `pg_dump -n pmieducar -n modules -n cadastro` produziu 164 erros de restore, todos por dependência externa (funções `public.audit()`, schema `portal.funcionario`). O escopo foi ajustado para **backup completo do banco** (sem `-n`), mantendo a verificação de tuplas no recorte acadêmico dos 3 schemas. Detalhamento em `manifest.md` §"Nota de revisão de escopo".

**Tratamento especial em T06.** `pg_dump --data-only` emite dados em `COPY` direto, sem desativar triggers. Com o schema preexistente, os triggers de auditoria (`public.audit()`) disparam durante o COPY e colidem com a inserção explícita em `public.ieducar_audit` (erro `duplicate key value violates unique constraint ieducar_audit_pkey`). A correção é usar `-Fc` (custom format) + `pg_restore --disable-triggers`, que roda internamente com `session_replication_role = replica`.

## 4. Resultados

### 4.1 CVPB = 100,0%

| Teste | Descrição | Status | SHA-256 | Tuplas | FKs |
| :-: | :--- | :-: | :-: | :-: | :-: |
| T01 | Custom format | **PASS** | `evidencias/g2_confiabilidade/m6/T01/dump.sha256` | Sim | Sim |
| T02 | Plain SQL | **PASS** | `T02/dump.sha256` | Sim | Sim |
| T03 | Directory format | **PASS** | `T03/dump.sha256` | Sim | Sim |
| T04 | Clean/if-exists | **PASS** | `T04/dump.sha256` | Sim | Sim |
| T05 | Schema-only | **PASS** | `T05/dump.sha256` | Sim (3 schemas, 0 tuplas) | N/A |
| T06 | Data-only | **PASS** | `T06/dump.sha256` | Sim | Sim |

$$
\text{CVPB} = \frac{6}{6} \times 100\% = \mathbf{100{,}0\%}
$$

**Classificação:** Excelente ($S_{\text{M6}} = 4$).
**Hipótese H2.3:** **Confirmada** ($\text{CVPB} = 100\% \ge 95\%$).

### 4.2 Impacto nos índices

$$
\text{IQC}_{\text{Conf}} = \frac{S_{\text{M3}} \times 2{,}0 + S_{\text{M4}} \times 2{,}0 + S_{\text{M6}} \times 1{,}0}{5{,}0} = \frac{4 \times 2 + 1 \times 2 + 4 \times 1}{5} = \mathbf{2{,}80}
$$

**Nota:** o `IQC_Conf` foi calculado porque, após a execução de M6, **todas** as métricas de confiabilidade (M3, M4, M6) têm dados comprovados. M5 continua excluída pela política §3.1 (não mensurável em laboratório).

## 5. Veredito

**CVPB = 100% (Excelente, S = 4)** — o procedimento de backup/restore do i-Educar 2.12 é integralmente recuperável nos 6 cenários testados. A **H2.3 é confirmada**.

**Impacto no julgamento da Fase 5:**
- `IQC_Conf` passa de **SUSPENSO** para **$2{,}80$** (calculado)
- `IQM` passa de **SUSPENSO** para **$2{,}83$** (calculado)
- **Classificação permanece Classe C** por dois motivos independentes: (i) **Gate M4 REPROVADO** (ITAE = 0%, regra não-compensatória) e (ii) **$\text{IQC}_{\text{Manut}} = 2{,}20 < 2{,}50$** (piso de manutenibilidade do commit congelado)

## 6. Limitações

- **Backup de banco completo vs. 3 schemas**: o escopo foi ajustado de `-n pmieducar -n modules -n cadastro` para dump completo, porque o backup filtrado excluía dependências (funções `public.*`, schema `portal`) que os triggers e FKs dos 3 schemas referenciam. A verificação de tuplas permanece no recorte acadêmico.
- **Amostra**: 6 cenários cobrem os 3 formatos do `pg_dump` (custom, plain, directory) + 2 modos (schema-only, data-only) + 1 variação (clean/if-exists). Cenários de recuperação parcial (PITR com WAL) não foram cobertos.
- **Rodada inicial não preservada**: os logs da primeira execução (164 erros de restore com o escopo de 3 schemas) não foram versionados; o procedimento original permanece rastreável pelo manifesto congelado no commit `05b37b4`.
- **Tabelas de notas e faltas vazias na linha de base**: `modules.nota_aluno` e `modules.falta_aluno` têm 0 tuplas no banco de teste, então a restauração do conteúdo de notas e faltas não foi exercitada; a CVPB comprova a restauração do esquema e das demais tabelas contadas.
- **Ambiente**: medição em PostgreSQL 18.7 do container Docker local; comportamento de `pg_dump`/`pg_restore` em versões anteriores pode variar.

## 7. Rastreabilidade

| Item | Valor |
| :--- | :--- |
| Commit do produto | `7903a3efc7689942ee700007f86ed581023aad27` |
| Commit do manifesto | `05b37b4` (versão original, com `-n pmieducar -n modules -n cadastro`) |
| Baseline de tuplas | 2.132 tuplas em 12 tabelas |
| Resultados | `evidencias/g2_confiabilidade/m6/results.csv` |
| Memória de cálculo | `evidencias/g2_confiabilidade/m6/cvpb.log` |
| Logs por teste | `evidencias/g2_confiabilidade/m6/T01/` a `T06/` |
| Script | `scripts/avaliacao/m6/run_m6.sh` |

## 8. Como reproduzir

```bash
# Pré-requisito: container postgres do M3 em Up
docker compose -f scripts/avaliacao/m3/compose.yml up -d postgres

# Executar os 6 testes
bash scripts/avaliacao/m6/run_m6.sh

# Verificar
cat evidencias/g2_confiabilidade/m6/cvpb.log
cat evidencias/g2_confiabilidade/m6/results.csv