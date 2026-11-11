#!/usr/bin/env bash
# M1 (TINCR) - verificacao de coexistencia entre as instancias A e B do i-Educar 2.12.
# Pre-requisito: ambas as instancias no ar (docker compose --env-file config/instancia-X.env up -d).
# Cada bloco imprime o comando executado e a saida bruta; nenhum valor e arbitrado.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

A="docker compose --env-file config/instancia-a.env"
B="docker compose --env-file config/instancia-b.env"

run() { echo; echo "\$ $*"; "$@" 2>&1 || echo "[exit=$?]"; }
sec() { echo; echo "=================== $* ==================="; }

sec "R1 container_name e R2 portas publicadas (docker ps)"
run docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'

sec "R3 imagem (tag) por instancia"
run docker images --format '{{.Repository}}:{{.Tag}}' --filter 'reference=ieducar-*-php'

sec "R4 servicos HTTP independentes (versao da API em cada porta)"
run python -c "
import urllib.request as u
for n,p in (('A',8080),('B',8081)):
    r=u.urlopen(f'http://localhost:{p}/api/version',timeout=60)
    print(n,p,r.status,r.headers.get('Content-Type'),r.read().decode())
"

sec "R5 banco de dados: DB_DATABASE e DB_USERNAME de cada instancia"
run $A exec -T postgres psql -U ieducar -d ieducar -Atc "select current_database(), current_user, (select count(*) from pg_database where datname='ieducar_b')"
run $B exec -T postgres psql -U ieducar_b -d ieducar_b -Atc "select current_database(), current_user, (select count(*) from pg_database where datname='ieducar')"

sec "R5b isolamento de dados: marcador gravado em B nao aparece em A"
run $B exec -T postgres psql -U ieducar_b -d ieducar_b -Atc "create table if not exists m1_marcador(origem text); insert into m1_marcador values ('instancia-b'); select count(*) from m1_marcador"
run $A exec -T postgres psql -U ieducar -d ieducar -Atc "select to_regclass('public.m1_marcador') is null as ausente_em_a"
run $B exec -T postgres psql -U ieducar_b -d ieducar_b -Atc "drop table m1_marcador"

sec "R6 Redis: prefixo de chaves REDIS_PREFIX (cache gravado pela aplicacao em cada instancia)"
run $A exec -T php php artisan tinker --execute="Cache::put('m1_probe','A',60); echo config('database.redis.options.prefix');"
run $B exec -T php php artisan tinker --execute="Cache::put('m1_probe','B',60); echo config('database.redis.options.prefix');"
run $A exec -T redis redis-cli -n 1 --scan --pattern '*m1_probe*'
run $B exec -T redis redis-cli -n 1 --scan --pattern '*m1_probe*'

sec "R7 Redis compartilhado hipotetico: colisao so ocorre sem prefixo distinto (A e B usam instancias Redis proprias)"
run $A exec -T redis redis-cli info keyspace
run $B exec -T redis redis-cli info keyspace

sec "R8 volume nomeado do PostgreSQL e R9 rede (escopo do projeto compose)"
run docker volume ls --format '{{.Name}}' --filter name=ieducar-
run docker network ls --format '{{.Name}}' --filter name=ieducar-

sec "R10 diretorio de armazenamento (bind mount do checkout, inclui storage/ e .env)"
run docker inspect ieducar-a-fpm --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
run docker inspect ieducar-b-fpm --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
