# Manifesto Congelado — M6 (CVPB)

**Issue:** #42
**Commit do produto:** 7903a3efc7689942ee700007f86ed581023aad27
**Data do congelamento:** 2026-11-15
**Ambiente:** scripts/avaliacao/m3/compose.yml (PostgreSQL 18.7)
**Banco de origem:** `testing`
**Banco de destino:** `ieducar_m6_restore` (isolado, criado por teste)

## Casos de teste planejados

| ID | Descrição | pg_dump | Restore | Critério de sucesso |
| :-: | :--- | :--- | :--- | :--- |
| T01 | Custom format | `-Fc -n pmieducar -n modules -n cadastro` | `pg_restore` em banco limpo | exit 0; SHA-256; tuplas batem; FKs íntegras |
| T02 | Plain SQL | `-Fp -n pmieducar -n modules -n cadastro` | `psql -f` em banco limpo | exit 0; tuplas batem; FKs íntegras |
| T03 | Directory format | `-Fd -n pmieducar -n modules -n cadastro` | `pg_restore` em banco limpo | exit 0; tuplas batem; FKs íntegras |
| T04 | Clean/if-exists | `-Fc --clean --if-exists` | `pg_restore` sobre banco populado | exit 0; após re-restore, tuplas batem |
| T05 | Schema-only | `--schema-only` | `pg_restore` em banco limpo | exit 0; 3 schemas; 0 tuplas |
| T06 | Data-only | `--data-only` | `pg_restore` em banco com schema (de T05) | exit 0; tuplas batem |

## Verificação por teste

1. Exit code `pg_dump` = 0
2. SHA-256 do dump gravado (`sha256sum`)
3. Exit code `pg_restore` = 0
4. Contagem de tuplas em 12 tabelas de referência = baseline
5. Integridade de FKs: 0 órfãos em `matricula`↔`aluno`, `matricula_turma`↔`matricula`, `nota_aluno`↔`matricula`

## Cálculo

CVPB = (N sucessos / 6) × 100%

Limiares: 100% = Excelente · [95,100) = Bom · [90,95) = Regular · <90% = Crítico

## Nota de revisão de escopo (antes da execução bem-sucedida)

A execução inicial com `pg_dump -n pmieducar -n modules -n cadastro` produziu 164 erros de
restore, todos por dependência externa: funções `public.audit()`, `public.update_updated_at()`,
`public.when_deleted_*()`, tabelas `public.document_absence_reasons`/`public.menus` e schema
`portal.funcionario`.

O backup de 3 schemas sem suas dependências **não é um backup recuperável**: o sistema ficaria
sem funções de auditoria, sem triggers de atualização, sem FKs para `portal.funcionario`. O
procedimento correto para medir Recuperabilidade (ISO/IEC 25010) é **backup completo do banco**.

**Escopo ajustado:** `pg_dump -Fc testing` (sem `-n`, todos os schemas) para todos os 6 testes.

**Commit do ajuste:** `c5606fc1c1c27baf9417a87d1947b31f5230603c`

**Desvio adicional no T06:** o manifesto original previa `pg_dump --data-only` restaurado em banco com o schema de T05. Na execução, os gatilhos de auditoria (`public.audit()`) dispararam durante o `COPY` e colidiram com a inserção explícita em `public.ieducar_audit` (`duplicate key value violates unique constraint ieducar_audit_pkey`). O T06 passou a usar `--data-only -Fc` com `pg_restore --disable-triggers`. A colisão é registrada como achado de recuperabilidade: a restauração somente de dados exige desativar os gatilhos de auditoria.

**Evidência da rodada inicial:** os logs da primeira execução (164 erros) não foram versionados. O procedimento original fica rastreável pelo commit `05b37b4`, que congelou este manifesto antes da execução.
