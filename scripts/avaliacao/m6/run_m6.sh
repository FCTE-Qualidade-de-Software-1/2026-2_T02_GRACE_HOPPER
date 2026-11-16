#!/usr/bin/env bash
# scripts/avaliacao/m6/run_m6.sh
# Executa os 6 casos de teste do manifesto M6 (CVPB) — versão corrigida
# Requer: container postgres do M3 em Up
set -uo pipefail

COMPOSE="scripts/avaliacao/m3/compose.yml"
EVID="evidencias/g2_confiabilidade/m6"
SRC_DB="testing"
DST_DB="ieducar_m6_restore"
PG_USER="ieducar_m3"

DC()       { docker compose -f "$COMPOSE" "$@"; }
PG_EXEC()  { DC exec -T postgres "$@"; }

# psql direto no container (stdin = SQL via heredoc)
PG_PSQL() {
  local db="$1"; shift
  DC exec -T postgres psql -U "$PG_USER" -d "$db" -A -t -v ON_ERROR_STOP=1 "$@"
}

mkdir -p "$EVID"

# ── Baseline de tuplas (referência) — via heredoc, DENTRO do container ──
echo "[setup] gerando baseline de tuplas..."
DC exec -T postgres psql -U "$PG_USER" -d "$SRC_DB" -A -t -v ON_ERROR_STOP=1 <<'SQL' \
  | grep -vE '^\s*$' | sort > /tmp/m6_baseline_tuples.txt
SELECT 'pmieducar.matricula', count(*) FROM pmieducar.matricula
UNION ALL SELECT 'pmieducar.aluno', count(*) FROM pmieducar.aluno
UNION ALL SELECT 'pmieducar.escola', count(*) FROM pmieducar.escola
UNION ALL SELECT 'pmieducar.turma', count(*) FROM pmieducar.turma
UNION ALL SELECT 'pmieducar.serie', count(*) FROM pmieducar.serie
UNION ALL SELECT 'pmieducar.curso', count(*) FROM pmieducar.curso
UNION ALL SELECT 'pmieducar.matricula_turma', count(*) FROM pmieducar.matricula_turma
UNION ALL SELECT 'modules.nota_aluno', count(*) FROM modules.nota_aluno
UNION ALL SELECT 'modules.falta_aluno', count(*) FROM modules.falta_aluno
UNION ALL SELECT 'modules.regra_avaliacao', count(*) FROM modules.regra_avaliacao
UNION ALL SELECT 'cadastro.pessoa', count(*) FROM cadastro.pessoa
UNION ALL SELECT 'cadastro.fisica', count(*) FROM cadastro.fisica
ORDER BY 1;
SQL

BASELINE_LINES=$(wc -l < /tmp/m6_baseline_tuples.txt)
echo "[setup] baseline: $BASELINE_LINES linhas"
if [ "$BASELINE_LINES" -ne 12 ]; then
  echo "ERRO: baseline incompleto (esperado 12 linhas, obtido $BASELINE_LINES)"
  exit 1
fi
cp /tmp/m6_baseline_tuples.txt "$EVID/baseline_tuples.txt"

drop_create_db() {
  # Conecta no DB maintenance `postgres` (não usa $DST_DB)
  DC exec -T postgres psql -U "$PG_USER" -d postgres -v ON_ERROR_STOP=1 \
    -c "DROP DATABASE IF EXISTS $DST_DB WITH (FORCE);" \
    -c "CREATE DATABASE $DST_DB;" || return 1
}

# Verifica tuplas + FKs no banco restaurado; retorna 0 se OK, 1 se qualquer divergência
verify_restored() {
  local outdir="$1"
  DC exec -T postgres psql -U "$PG_USER" -d "$DST_DB" -A -t -v ON_ERROR_STOP=1 <<'SQL' > "$outdir/verify_tuples.log" 2>"$outdir/verify_tuples.err"
SELECT 'pmieducar.matricula', count(*) FROM pmieducar.matricula
UNION ALL SELECT 'pmieducar.aluno', count(*) FROM pmieducar.aluno
UNION ALL SELECT 'pmieducar.escola', count(*) FROM pmieducar.escola
UNION ALL SELECT 'pmieducar.turma', count(*) FROM pmieducar.turma
UNION ALL SELECT 'pmieducar.serie', count(*) FROM pmieducar.serie
UNION ALL SELECT 'pmieducar.curso', count(*) FROM pmieducar.curso
UNION ALL SELECT 'pmieducar.matricula_turma', count(*) FROM pmieducar.matricula_turma
UNION ALL SELECT 'modules.nota_aluno', count(*) FROM modules.nota_aluno
UNION ALL SELECT 'modules.falta_aluno', count(*) FROM modules.falta_aluno
UNION ALL SELECT 'modules.regra_avaliacao', count(*) FROM modules.regra_avaliacao
UNION ALL SELECT 'cadastro.pessoa', count(*) FROM cadastro.pessoa
UNION ALL SELECT 'cadastro.fisica', count(*) FROM cadastro.fisica
ORDER BY 1;
SQL
  # Normaliza e compara com o baseline
  grep -vE '^\s*$' "$outdir/verify_tuples.log" | sort > "$outdir/verify_tuples.sorted"
  diff -u /tmp/m6_baseline_tuples.txt "$outdir/verify_tuples.sorted" > "$outdir/tuples_diff.log" 2>&1
  local tuples_ok=0
  [ ! -s "$outdir/tuples_diff.log" ] && [ -s "$outdir/verify_tuples.sorted" ] && tuples_ok=1

  DC exec -T postgres psql -U "$PG_USER" -d "$DST_DB" -A -t -v ON_ERROR_STOP=1 <<'SQL' > "$outdir/verify_fks.log" 2>"$outdir/verify_fks.err"
SELECT 'orfao_matricula_sem_aluno', count(*) FROM pmieducar.matricula m
  LEFT JOIN pmieducar.aluno a ON a.cod_aluno = m.ref_cod_aluno
  WHERE a.cod_aluno IS NULL
UNION ALL SELECT 'orfao_turma_sem_matricula', count(*) FROM pmieducar.matricula_turma mt
  LEFT JOIN pmieducar.matricula m ON m.cod_matricula = mt.ref_cod_matricula
  WHERE m.cod_matricula IS NULL
UNION ALL SELECT 'orfao_nota_sem_matricula', count(*) FROM modules.nota_aluno na
  LEFT JOIN pmieducar.matricula m ON m.cod_matricula = na.matricula_id
  WHERE m.cod_matricula IS NULL
UNION ALL SELECT 'orfao_falta_sem_matricula', count(*) FROM modules.falta_aluno fa
  LEFT JOIN pmieducar.matricula m ON m.cod_matricula = fa.matricula_id
  WHERE m.cod_matricula IS NULL
ORDER BY 1;
SQL
  local fk_ok=0
  if ! grep -qE '\|[1-9]' "$outdir/verify_fks.log"; then
    fk_ok=1
  fi

  [ "$tuples_ok" -eq 1 ] && [ "$fk_ok" -eq 1 ]
}

# ─── T01: custom format ───
test_T01() {
  local outdir="$EVID/T01"; rm -rf "$outdir"; mkdir -p "$outdir"
    PG_EXEC pg_dump -U "$PG_USER" -d "$SRC_DB" -Fc -f /tmp/m6_T01.dump \
    > "$outdir/dump.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sha256sum /tmp/m6_T01.dump > "$outdir/dump.sha256" 2>&1
  drop_create_db || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC pg_restore -U "$PG_USER" -d "$DST_DB" --no-owner --no-privileges --no-comments \
    /tmp/m6_T01.dump > "$outdir/restore.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  verify_restored "$outdir" && echo PASS > "$outdir/status.txt" || echo FAIL > "$outdir/status.txt"
}

# ─── T02: plain SQL ───
test_T02() {
  local outdir="$EVID/T02"; rm -rf "$outdir"; mkdir -p "$outdir"
    PG_EXEC pg_dump -U "$PG_USER" -d "$SRC_DB" -Fp -f /tmp/m6_T02.sql \
    > "$outdir/dump.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sha256sum /tmp/m6_T02.sql > "$outdir/dump.sha256" 2>&1
  drop_create_db || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sh -c "psql -U $PG_USER -d $DST_DB -v ON_ERROR_STOP=1 -f /tmp/m6_T02.sql" \
    > "$outdir/restore.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  verify_restored "$outdir" && echo PASS > "$outdir/status.txt" || echo FAIL > "$outdir/status.txt"
}

# ─── T03: directory format ───
test_T03() {
  local outdir="$EVID/T03"; rm -rf "$outdir"; mkdir -p "$outdir"
  PG_EXEC rm -rf /tmp/m6_T03.dir
    PG_EXEC pg_dump -U "$PG_USER" -d "$SRC_DB" -Fd -f /tmp/m6_T03.dir \
    > "$outdir/dump.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sh -c "find /tmp/m6_T03.dir -type f -exec sha256sum {} \\;" | sort > "$outdir/dump.sha256" 2>&1
  drop_create_db || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC pg_restore -U "$PG_USER" -d "$DST_DB" --no-owner --no-privileges --no-comments \
    /tmp/m6_T03.dir > "$outdir/restore.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  verify_restored "$outdir" && echo PASS > "$outdir/status.txt" || echo FAIL > "$outdir/status.txt"
}

# ─── T04: clean/if-exists sobre banco já populado ───
test_T04() {
  local outdir="$EVID/T04"; rm -rf "$outdir"; mkdir -p "$outdir"
    PG_EXEC pg_dump -U "$PG_USER" -d "$SRC_DB" -Fc -f /tmp/m6_T04.dump \
    > "$outdir/dump.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sha256sum /tmp/m6_T04.dump > "$outdir/dump.sha256" 2>&1
  drop_create_db || { echo FAIL > "$outdir/status.txt"; return; }
  # 1º restore: banco limpo (popula)
  PG_EXEC pg_restore -U "$PG_USER" -d "$DST_DB" --no-owner --no-privileges --no-comments \
    /tmp/m6_T04.dump > "$outdir/restore_1_populate.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  # 2º restore: --clean --if-exists sobre banco populado
  PG_EXEC pg_restore -U "$PG_USER" -d "$DST_DB" --no-owner --no-privileges --no-comments \
    --clean --if-exists /tmp/m6_T04.dump > "$outdir/restore_2_clean.log" 2>&1 \
    || { echo FAIL > "$outdir/status.txt"; return; }
  verify_restored "$outdir" && echo PASS > "$outdir/status.txt" || echo FAIL > "$outdir/status.txt"
}

# ─── T05: schema-only (3 schemas, 0 tuplas) ───
test_T05() {
  local outdir="$EVID/T05"; rm -rf "$outdir"; mkdir -p "$outdir"
    PG_EXEC pg_dump -U "$PG_USER" -d "$SRC_DB" --schema-only -f /tmp/m6_T05.sql \
    > "$outdir/dump.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sha256sum /tmp/m6_T05.sql > "$outdir/dump.sha256" 2>&1
  drop_create_db || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sh -c "psql -U $PG_USER -d $DST_DB -v ON_ERROR_STOP=1 -f /tmp/m6_T05.sql" \
    > "$outdir/restore.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }

  # Verificar 3 schemas + 0 tuplas em cada tabela
  DC exec -T postgres psql -U "$PG_USER" -d "$DST_DB" -A -t -v ON_ERROR_STOP=1 <<'SQL' \
    > "$outdir/verify_schemas.log" 2>&1
SELECT nspname FROM pg_namespace WHERE nspname IN ('pmieducar','modules','cadastro') ORDER BY 1;
SQL
  DC exec -T postgres psql -U "$PG_USER" -d "$DST_DB" -A -t -v ON_ERROR_STOP=1 <<'SQL' \
    > "$outdir/verify_tuples.log" 2>&1
SELECT 'pmieducar.matricula', count(*) FROM pmieducar.matricula
UNION ALL SELECT 'pmieducar.aluno', count(*) FROM pmieducar.aluno
UNION ALL SELECT 'pmieducar.escola', count(*) FROM pmieducar.escola
UNION ALL SELECT 'pmieducar.turma', count(*) FROM pmieducar.turma
UNION ALL SELECT 'pmieducar.serie', count(*) FROM pmieducar.serie
UNION ALL SELECT 'pmieducar.curso', count(*) FROM pmieducar.curso
UNION ALL SELECT 'pmieducar.matricula_turma', count(*) FROM pmieducar.matricula_turma
UNION ALL SELECT 'modules.nota_aluno', count(*) FROM modules.nota_aluno
UNION ALL SELECT 'modules.falta_aluno', count(*) FROM modules.falta_aluno
UNION ALL SELECT 'modules.regra_avaliacao', count(*) FROM modules.regra_avaliacao
UNION ALL SELECT 'cadastro.pessoa', count(*) FROM cadastro.pessoa
UNION ALL SELECT 'cadastro.fisica', count(*) FROM cadastro.fisica
ORDER BY 1;
SQL

  local schemas_ok=0 nonzero=0
  [ "$(grep -cE '^(pmieducar|modules|cadastro)$' "$outdir/verify_schemas.log")" -eq 3 ] && schemas_ok=1
  nonzero=$(grep -vE '^\s*$' "$outdir/verify_tuples.log" | awk -F'|' '$2+0 > 0' | wc -l)
  [ "$schemas_ok" -eq 1 ] && [ "$nonzero" -eq 0 ] \
    && echo PASS > "$outdir/status.txt" || echo FAIL > "$outdir/status.txt"
}

# ─── T06: data-only (schema de T05 + data) ───
test_T06() {
  local outdir="$EVID/T06"; rm -rf "$outdir"; mkdir -p "$outdir"
  # Data-only em formato custom (-Fc) para usar pg_restore
  PG_EXEC pg_dump -U "$PG_USER" -d "$SRC_DB" --data-only -Fc -f /tmp/m6_T06.dump \
    > "$outdir/dump.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  PG_EXEC sha256sum /tmp/m6_T06.dump > "$outdir/dump.sha256" 2>&1
  drop_create_db || { echo FAIL > "$outdir/status.txt"; return; }
  # 1º: schema-only de T05 (recria todas as tabelas + triggers + FKs)
  PG_EXEC sh -c "psql -U $PG_USER -d $DST_DB -v ON_ERROR_STOP=1 -f /tmp/m6_T05.sql" \
    > "$outdir/restore_schema.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  # 2º: data-only com --disable-triggers (evita a colisão em public.ieducar_audit)
  PG_EXEC pg_restore -U "$PG_USER" -d "$DST_DB" --data-only --disable-triggers \
    --no-owner --no-privileges --no-comments /tmp/m6_T06.dump \
    > "$outdir/restore_data.log" 2>&1 || { echo FAIL > "$outdir/status.txt"; return; }
  verify_restored "$outdir" && echo PASS > "$outdir/status.txt" || echo FAIL > "$outdir/status.txt"
}

# ─── Execução ───
echo "=========================================="
echo "M6 CVPB — 6 casos de teste"
echo "=========================================="

for t in T01 T02 T03 T04 T05 T06; do
  echo ""
  echo ">>> Executando $t..."
  test_$t
  status=$(cat "$EVID/$t/status.txt" 2>/dev/null || echo "MISSING")
  echo "<<< $t: $status"
done

# ─── Consolidação ───
echo ""
echo "=========================================="
echo "Resultados"
echo "=========================================="

successes=0
total=6
for t in T01 T02 T03 T04 T05 T06; do
  status=$(cat "$EVID/$t/status.txt" 2>/dev/null || echo "MISSING")
  echo "$t: $status"
  [ "$status" = "PASS" ] && successes=$((successes + 1))
done

CVPB=$(awk "BEGIN {printf \"%.2f\", $successes / $total * 100}")
echo ""
echo "Sucessos: $successes / $total"
echo "CVPB: $CVPB%"

{
  echo "teste,descricao,status"
  echo "T01,custom format,$(cat $EVID/T01/status.txt 2>/dev/null || echo MISSING)"
  echo "T02,plain SQL,$(cat $EVID/T02/status.txt 2>/dev/null || echo MISSING)"
  echo "T03,directory format,$(cat $EVID/T03/status.txt 2>/dev/null || echo MISSING)"
  echo "T04,clean/if-exists,$(cat $EVID/T04/status.txt 2>/dev/null || echo MISSING)"
  echo "T05,schema-only,$(cat $EVID/T05/status.txt 2>/dev/null || echo MISSING)"
  echo "T06,data-only,$(cat $EVID/T06/status.txt 2>/dev/null || echo MISSING)"
} > "$EVID/results.csv"

{
  echo "M6 CVPB — Memória de cálculo"
  echo "Data: $(date -Iseconds)"
  echo "Sucessos: $successes"
  echo "Total: $total"
  echo "CVPB = $successes/$total × 100 = $CVPB%"
  echo ""
  echo "Por teste:"
  for t in T01 T02 T03 T04 T05 T06; do
    echo "  $t: $(cat $EVID/$t/status.txt 2>/dev/null || echo MISSING)"
  done
} | tee "$EVID/cvpb.log"

echo ""
echo "Resultado salvo em $EVID/cvpb.log"